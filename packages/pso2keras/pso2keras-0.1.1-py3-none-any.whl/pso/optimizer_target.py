import gc
import json
import os
import sys
from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm

from .particle import Particle

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        # tf.config.experimental.set_visible_devices(gpus[0], "GPU")
        # print(tf.config.experimental.get_visible_devices("GPU"))
        tf.config.experimental.set_memory_growth(gpus[0], True)
        # print("set memory growth")
    except RuntimeError as e:
        print(e)


class Optimizer_Target:
    """
    particle swarm optimization
    PSO 실행을 위한 클래스
    """

    def __init__(
        self,
        model: keras.models,
        loss="mse",
        n_particles: int = 10,
        c0=0.5,
        c1=1.5,
        w_min=0.5,
        w_max=1.5,
        negative_swarm: float = 0,
        mutation_swarm: float = 0,
        np_seed: int = None,
        tf_seed: int = None,
        target_weights=None,
    ):
        """
        particle swarm optimization

        Args:
            model (keras.models): 모델 구조
            loss (str): 손실함수
            n_particles (int): 파티클 개수
            c0 (float): local rate - 지역 최적값 관성 수치
            c1 (float): global rate - 전역 최적값 관성 수치
            w_min (float): 최소 관성 수치
            w_max (float): 최대 관성 수치
            negative_swarm (float): 최적해와 반대로 이동할 파티클 비율 - 0 ~ 1 사이의 값
            mutation_swarm (float): 돌연변이가 일어날 확률
            np_seed (int, optional): numpy seed. Defaults to None.
            tf_seed (int, optional): tensorflow seed. Defaults to None.
            target_weights (list, optional): 목표 가중치. Defaults to None.
        """
        if np_seed is not None:
            np.random.seed(np_seed)
        if tf_seed is not None:
            tf.random.set_seed(tf_seed)

        self.model = model  # 모델 구조
        self.loss = loss  # 손실함수
        self.n_particles = n_particles  # 파티클 개수
        self.particles = [None] * n_particles  # 파티클 리스트
        self.c0 = c0  # local rate - 지역 최적값 관성 수치
        self.c1 = c1  # global rate - 전역 최적값 관성 수치
        self.w_min = w_min  # 최소 관성 수치
        self.w_max = w_max  # 최대 관성 수치
        self.negative_swarm = negative_swarm  # 최적해와 반대로 이동할 파티클 비율 - 0 ~ 1 사이의 값
        self.mutation_swarm = mutation_swarm  # 관성을 추가로 사용할 파티클 비율 - 0 ~ 1 사이의 값
        self.g_best_score = [0, np.inf]  # 최고 점수 - 시작은 0으로 초기화
        self.g_best = None  # 최고 점수를 받은 가중치
        self.g_best_ = None  # 최고 점수를 받은 가중치 - 값의 분산을 위한 변수
        self.target_weights = target_weights  # 목표 가중치
        self.avg_score = 0  # 평균 점수

        self.save_path = None  # 저장 위치
        self.renewal = "acc"
        self.Dispersion = False
        self.day = datetime.now().strftime("%m-%d-%H-%M")

        negative_count = 0

        for i in tqdm(range(self.n_particles), desc="Initializing Particles"):
            m = keras.models.model_from_json(model.to_json())
            init_weights = m.get_weights()
            w_, sh_, len_ = self._encode(init_weights)
            w_ = np.random.uniform(-1, 2, len(w_))
            m.set_weights(self._decode(w_, sh_, len_))
            m.compile(loss=self.loss, optimizer="sgd", metrics=["accuracy"])
            self.particles[i] = Particle(
                m,
                loss,
                negative=True if i < negative_swarm * self.n_particles else False,
                mutation=mutation_swarm,
            )
            if i < negative_swarm * self.n_particles:
                negative_count += 1

        print(f"negative swarm : {negative_count} / {self.n_particles}")
        print(
            f"mutation swarm : {mutation_swarm * self.n_particles} / {self.n_particles}"
        )

        gc.collect()

    def __del__(self):
        del self.model
        del self.loss
        del self.n_particles
        del self.particles
        del self.c0
        del self.c1
        del self.w_min
        del self.w_max
        del self.negative_swarm
        del self.g_best_score
        del self.g_best
        del self.g_best_
        del self.avg_score
        gc.collect()

    def _encode(self, weights):
        """
        가중치를 1차원으로 풀어서 반환

        Args:
            weights (list) : keras model의 가중치
        Returns:
            (numpy array) : 가중치 - 1차원으로 풀어서 반환
            (list) : 가중치의 원본 shape
            (list) : 가중치의 원본 shape의 길이
        """
        w_gpu = np.array([])
        length = []
        shape = []
        for layer in weights:
            shape.append(layer.shape)
            w_ = layer.reshape(-1)
            length.append(len(w_))
            w_gpu = np.append(w_gpu, w_)

        del weights

        return w_gpu, shape, length

    def _decode(self, weight, shape, length):
        """
        _encode 로 인코딩된 가중치를 원본 shape으로 복원
        파라미터는 encode의 리턴값을 그대로 사용을 권장

        Args:
            weight (numpy array): 가중치 - 1차원으로 풀어서 반환
            shape (list): 가중치의 원본 shape
            length (list): 가중치의 원본 shape의 길이
        Returns:
            (list) : 가중치 원본 shape으로 복원
        """
        weights = []
        start = 0
        for i in range(len(shape)):
            end = start + length[i]
            w_ = weight[start:end]
            w_ = np.reshape(w_, shape[i])
            weights.append(w_)
            start = end

        del weight
        del shape
        del length

        return weights

    def f(self, x, y, weights):
        """
        EBPSO의 목적함수 (예상)

        Args:
            x (list): 입력 데이터
            y (list): 출력 데이터
            weights (list): 가중치

        Returns:
            (float): 목적 함수 값
        """
        self.model.set_weights(weights)
        self.model.compile(loss=self.loss, optimizer="sgd", metrics=["accuracy"])
        score = self.model.evaluate(x, y, verbose=0)[1]
        if score > 0:
            return 1 / (1 + score)
        else:
            return 1 + np.abs(score)

    def fit(
        self,
        x,
        y,
        epochs: int = 100,
        save: bool = False,
        save_path: str = "./result",
        renewal: str = "acc",
        empirical_balance: bool = False,
        Dispersion: bool = False,
        check_point: int = None,
    ):
        """
        Args:
            x_test : numpy array,
            y_test : numpy array,
            epochs : int,
            save : bool - True : save, False : not save
            save_path : str ex) "./result",
            renewal : str ex) "acc" or "loss" or "both",
            empirical_balance : bool - True :
            Dispersion : bool - True : g_best 의 값을 분산시켜 전역해를 찾음, False : g_best 의 값만 사용
            check_point : int - 저장할 위치 - None : 저장 안함
        """
        self.save_path = save_path
        self.empirical_balance = empirical_balance
        self.Dispersion = Dispersion

        self.renewal = renewal

        try:
            if save:
                if save_path is None:
                    raise ValueError("save_path is None")
                else:
                    self.save_path = save_path
                    if not os.path.exists(save_path):
                        os.makedirs(save_path, exist_ok=True)
        except ValueError as e:
            print(e)
            sys.exit(1)

        for i in tqdm(range(self.n_particles), desc="Initializing velocity"):
            p = self.particles[i]
            local_score = p.get_score(x, y, renewal=renewal)

            if renewal == "acc":
                if local_score[1] > self.g_best_score[0]:
                    self.g_best_score[0] = local_score[1]
                    self.g_best = p.get_best_weights()
                    self.g_best_ = p.get_best_weights()
            elif renewal == "loss":
                if local_score[0] < self.g_best_score[1]:
                    self.g_best_score[1] = local_score[0]
                    self.g_best = p.get_best_weights()
                    self.g_best_ = p.get_best_weights()

            if local_score[0] == None:
                local_score[0] = np.inf

            if local_score[1] == None:
                local_score[1] = 0

            if save:
                with open(
                    f"./{save_path}/{self.day}_{self.n_particles}_{epochs}_{self.c0}_{self.c1}_{self.w_min}_{renewal}.csv",
                    "a",
                ) as f:
                    f.write(f"{local_score[0]}, {local_score[1]}")
                    if i != self.n_particles - 1:
                        f.write(", ")
                    else:
                        f.write("\n")

                    f.close()
            del local_score
            gc.collect()

        print(
            f"initial g_best_score : {self.g_best_score[0] if self.renewal == 'acc' else self.g_best_score[1]}"
        )

        try:
            epochs_pbar = tqdm(
                range(epochs),
                desc=f"best {self.g_best_score[0]:.4f}|{self.g_best_score[1]:.4f}",
                ascii=True,
                leave=True,
            )
            for epoch in epochs_pbar:
                acc = 0
                loss = 0
                min_score = np.inf
                max_score = 0
                min_loss = np.inf
                max_loss = 0

                ts = self.c0 + np.random.rand() * (self.c1 - self.c0)

                part_pbar = tqdm(
                    range(len(self.particles)),
                    desc=f"acc : {max_score:.4f} loss : {min_loss:.4f}",
                    ascii=True,
                    leave=False,
                )
                for i in part_pbar:
                    part_pbar.set_description(
                        f"acc : {max_score:.4f} loss : {min_loss:.4f}"
                    )
                    w = self.w_max - (self.w_max - self.w_min) * epoch / epochs

                    g_, g_sh, g_len = self._encode(self.g_best)
                    decrement = (epochs - (epoch) + 1) / epochs
                    g_ = (1 - decrement) * g_ + decrement * ts
                    self.g_best_ = self._decode(g_, g_sh, g_len)

                    self.g_best = self.target_weights.get_weights()

                    if Dispersion:
                        g_best = self.g_best_
                    else:
                        g_best = self.g_best

                    if empirical_balance:
                        if np.random.rand() < np.exp(-(epoch) / epochs):
                            w_p_ = self.f(x, y, self.particles[i].get_best_weights())
                            w_g_ = self.f(x, y, self.g_best)
                            w_p = w_p_ / (w_p_ + w_g_)
                            w_g = w_p_ / (w_p_ + w_g_)

                            del w_p_
                            del w_g_

                        else:
                            p_b = self.particles[i].get_best_score()
                            g_a = self.avg_score
                            l_b = p_b - g_a
                            l_b = np.sqrt(np.power(l_b, 2))
                            p_ = (
                                1
                                / (self.n_particles * np.linalg.norm(self.c1 - self.c0))
                                * l_b
                            )
                            p_ = np.exp(-1 * p_)
                            w_p = p_
                            w_g = 1 - p_

                            del p_b
                            del g_a
                            del l_b
                            del p_

                        score = self.particles[i].step_w(
                            x, y, self.c0, self.c1, w, g_best, w_p, w_g, renewal=renewal
                        )

                    else:
                        score = self.particles[i].step(
                            x, y, self.c0, self.c1, w, g_best, renewal=renewal
                        )

                    if renewal == "acc":
                        if score[1] >= self.g_best_score[0]:
                            if score[1] > self.g_best_score[0]:
                                self.g_best_score[0] = score[1]
                                self.g_best = self.particles[i].get_best_weights()
                            else:
                                if score[0] < self.g_best_score[1]:
                                    self.g_best_score[1] = score[0]
                                    self.g_best = self.particles[i].get_best_weights()
                            epochs_pbar.set_description(
                                f"best {self.g_best_score[0]:.4f} | {self.g_best_score[1]:.4f}"
                            )
                    elif renewal == "loss":
                        if score[0] <= self.g_best_score[1]:
                            if score[0] < self.g_best_score[1]:
                                self.g_best_score[1] = score[0]
                                self.g_best = self.particles[i].get_best_weights()
                            else:
                                if score[1] > self.g_best_score[0]:
                                    self.g_best_score[0] = score[1]
                                    self.g_best = self.particles[i].get_best_weights()
                            epochs_pbar.set_description(
                                f"best {self.g_best_score[0]:.4f} | {self.g_best_score[1]:.4f}"
                            )

                    if score[0] == None:
                        score[0] = np.inf
                    if score[1] == None:
                        score[1] = 0

                    loss = loss + score[0]
                    acc = acc + score[1]

                    if score[0] < min_loss:
                        min_loss = score[0]
                    if score[0] > max_loss:
                        max_loss = score[0]

                    if score[1] < min_score:
                        min_score = score[1]
                    if score[1] > max_score:
                        max_score = score[1]

                    if save:
                        with open(
                            f"./{save_path}/{self.day}_{self.n_particles}_{epochs}_{self.c0}_{self.c1}_{self.w_min}_{renewal}.csv",
                            "a",
                        ) as f:
                            f.write(f"{score[0]}, {score[1]}")
                            if i != self.n_particles - 1:
                                f.write(", ")
                            else:
                                f.write("\n")
                        f.close()

                if check_point is not None:
                    if epoch % check_point == 0:
                        os.makedirs(f"./{save_path}/{self.day}", exist_ok=True)
                        self._check_point_save(f"./{save_path}/{self.day}/ckpt-{epoch}")
                self.avg_score = acc / self.n_particles

                gc.collect()

        except KeyboardInterrupt:
            print("Ctrl + C : Stop Training")
        except MemoryError:
            print("Memory Error : Stop Training")
        except Exception as e:
            print(e)
        finally:
            self.model_save(save_path)
            print("model save")
            self.save_info(save_path)
            print("save info")

            return self.g_best_score

    def get_best_model(self):
        """
        최고 점수를 받은 모델을 반환

        Returns:
            (keras.models): 모델
        """
        model = keras.models.model_from_json(self.model.to_json())
        model.set_weights(self.g_best)
        model.compile(loss=self.loss, optimizer="sgd", metrics=["accuracy"])
        return model

    def get_best_score(self):
        """
        최고 점수를 반환

        Returns:
            (float): 점수
        """
        return self.g_best_score

    def get_best_weights(self):
        """
        최고 점수를 받은 가중치를 반환

        Returns:
            (float): 가중치
        """
        return self.g_best

    def save_info(self, path: str = "./result"):
        """
        학습 정보를 저장

        Args:
            path (str, optional): 저장 위치. Defaults to "./result".
        """
        json_save = {
            "name": f"{self.day}_{self.n_particles}_{self.c0}_{self.c1}_{self.w_min}.h5",
            "n_particles": self.n_particles,
            "score": self.g_best_score,
            "c0": self.c0,
            "c1": self.c1,
            "w_min": self.w_min,
            "w_max": self.w_max,
            "loss_method": self.loss,
            "empirical_balance": self.empirical_balance,
            "Dispersion": self.Dispersion,
            "negative_swarm": self.negative_swarm,
            "mutation_swarm": self.mutation_swarm,
            "renewal": self.renewal,
        }

        with open(
            f"./{path}/{self.day}/{self.loss}_{self.g_best_score}.json",
            "a",
        ) as f:
            json.dump(json_save, f, indent=4)

        f.close()

    def _check_point_save(self, save_path: str = f"./result/check_point"):
        """
        중간 저장

        Args:
            save_path (str, optional): checkpoint 저장 위치 및 이름. Defaults to f"./result/check_point".
        """
        model = self.get_best_model()
        model.save_weights(save_path)

    def model_save(self, save_path: str = "./result"):
        """
        최고 점수를 받은 모델 저장

        Args:
            save_path (str, optional): 모델의 저장 위치. Defaults to "./result".

        Returns:
            (keras.models): 모델
        """
        model = self.get_best_model()
        model.save(
            f"./{save_path}/{self.day}/{self.n_particles}_{self.c0}_{self.c1}_{self.w_min}.h5"
        )
        return model
