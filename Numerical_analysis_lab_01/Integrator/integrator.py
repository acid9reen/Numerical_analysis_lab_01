import numpy as np


class Point_info:
    def __init__(self, step, x, v,
                 v2=None, lee=None,
                 mul_count=None, div_count=None) -> None:
        self.step = step
        self.x = x
        self.v = v
        self.v2 = v2
        self.delta_v2_v = v - v2 if v2 else None
        self.lee = lee
        self.mul_count = mul_count
        self.div_count = div_count

    def all(self):
        return (self.x, self.v, self.v2, self.delta_v2_v,
                self.lee, self.step, self.mul_count, self.div_count)


class Integrator:
    def __init__(self, func, step, eps, max_iters) -> None:
        self._func = func
        self._step = step
        self._eps = eps
        self._max_iters = max_iters

        self._mul_count = 0
        self._div_count = 0
        self._max_error = 0
        self._first_point_flag = True

        self.max_error = 0
        self.max_step = step
        self.max_step_x_coord = 0
        self.min_step = step
        self.min_step_x_coord = 0


    @staticmethod
    def test_task_1(x: float, u: float) -> float:
        return float(2 * u)


    @staticmethod
    def test_task_1_true_solution(x: float, u: float) -> float:
        return float(1 * np.exp(2 * x))


    @staticmethod
    def task_1(x: float, u: float) -> float:
        return float(((np.power(x, 3) + 1) / (np.power(x, 5) + 1))
                     * np.power(u, 2) + u - np.power(u, 3) * np.sin(10 * x))


    def _runge_kutta_4(self, x: float, v: float, step: float) -> dict:
        k1 = self._func(x, v)
        k2 = self._func(x + step / 2.0, v + 0.5 * step * k1)
        k3 = self._func(x + step / 2.0, v + 0.5 * step * k2)
        k4 = self._func(x + step, v + step * k3)

        v_next = v + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x_next = x + step

        return {'x': x_next, 'v': v_next}


    def next_point(self, x: float, v: float) -> Point_info:
        if self._first_point_flag:
            self._first_point_flag = False
            return Point_info(0, x, v)

        x_next, v_next = self._runge_kutta_4(x, v, self._step).values()

        return Point_info(self._step, x_next, v_next)


    def next_point_with_step_control(self, x: float, v: float) -> Point_info:
        if self._first_point_flag:
            self._first_point_flag = False
            return Point_info(0, x, v)

        iter_counter = 0

        while True:
            old_step = self._step

            whole_step = self._runge_kutta_4(x, v, self._step)
            half_step_1 = self._runge_kutta_4(x, v, self._step / 2.)
            half_step_2 = self._runge_kutta_4(half_step_1['x'], half_step_1['v'],
                                              self._step / 2.)

            delta = whole_step['v'] - half_step_2['v']
            lee = abs(delta / (np.power(2, 4) - 1))

            if (lee > self._eps) and (iter_counter < self._max_iters):
                self._step /= 2
                self._div_count += 1
                iter_counter += 1
            else:
                x_next = x + self._step
                v_next = whole_step['v']
                v2_next = half_step_2['v']

                if (lee < self._eps / np.power(2, 4 + 1)):
                    self._step *= 2
                    self._mul_count += 1

                if lee > self._max_error:
                    self.max_error = lee

                if self._step > self.max_step:
                    self.max_step = self._step
                    self.max_step_x_coord = x_next

                if self._step < self.min_step:
                    self.min_step = self._step
                    self.min_step_x_coord = x_next

                break

        return Point_info(old_step, x_next, v_next, v2_next,
                        lee, self._mul_count, self._div_count)
