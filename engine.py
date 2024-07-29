import numpy as np
import time
from math import sin, cos, pi


class DIPC:
    def __init__(
        self,
        g=10,
        u=0,
        m0=10,
        m1=5,
        m2=5,
        L1=1,
        L2=1,
        h=0.5,
        w=1,
        theta0=0,
        theta1=0.1,
        theta2=0.1,
        w0=0,
        w1=0,
        w2=0,
        dt=0.002,
        f1=0.01,
        f2=0.01,
    ):
        self.dt = dt
        self.h, self.w = (h, w)
        self.g, self.u, self.f1, self.f2 = (g, u, f1, f2)
        self.half = 0.5
        self.m0, self.m1, self.m2 = (m0, m1, m2)
        self.L1, self.L2 = (L1, L2)
        self.l1, self.l2 = (L1 / 2, L2 / 2)
        self.I1, self.I2 = (m1 * L1**2 / 12, m2 * L2**2 / 12)
        self.theta0, self.theta1, self.theta2 = (theta0, theta1, theta2)
        self.w0, self.w1, self.w2 = (w0, w1, w2)
        self.a0, self.a1, self.a2 = ("a0", "a1", "a2")

    def update(self):
        # bounds
        if self.theta0 > 4:
            self.theta0 = 4
            self.w0 = 0
        if self.theta0 < -4:
            self.theta0 = -4
            self.w0 = 0

        # numpy solve for accelerations
        m1l1m2L1 = self.m1 * self.l1 + self.m2 * self.L1
        coefficient = [
            [
                self.m0 + self.m1 + self.m2,
                m1l1m2L1 * cos(self.theta1),
                self.m2 * self.l2 * cos(self.theta2),
            ],
            [
                m1l1m2L1 * cos(self.theta1),
                self.m2 * self.l1**2 + self.m2 * self.L1**2 + self.I1,
                self.m2 * self.L1 * self.l2 * cos(self.theta1 - self.theta2),
            ],
            [
                self.m2 * self.l2 * cos(self.theta2),
                self.m2 * self.L1 * self.l2 * cos(self.theta1 - self.theta2),
                self.m2 * self.l2**2 + self.I2,
            ],
        ]

        const = [
            self.u
            + m1l1m2L1 * sin(self.theta1) * self.w1**2
            + self.m2 * self.l2 * sin(self.theta2) * self.w2**2,
            m1l1m2L1 * self.g * sin(self.theta1)
            - self.m2 * self.L1 * self.l2 * sin(self.theta1 - self.theta2) * self.w2**2,
            self.m2 * self.L1 * self.l2 * sin(self.theta1 - self.theta2) * self.w1**2
            + self.m2 * self.l2 * self.g * sin(self.theta2),
        ]

        self.sols = np.linalg.solve(coefficient, const)

        # update velocities and angles
        self.w0 += self.sols[0] * self.dt
        self.w1 += self.sols[1] * self.dt
        self.w2 += self.sols[2] * self.dt

        self.w0 *= 1 - self.f1
        self.w1 *= 1 - self.f2
        self.w2 *= 1 - self.f2

        self.theta0 += self.w0 * self.dt
        self.theta1 += self.w1 * self.dt
        self.theta2 += self.w2 * self.dt

        self.x0, self.y0 = (self.theta0, self.h // 2)
        self.x1, self.y1 = (
            self.x0 + self.L1 * sin(self.theta1),
            self.h + self.L1 * cos(self.theta1),
        )
        self.x2, self.y2 = (
            self.x1 + self.L2 * sin(self.theta2),
            self.y1 + self.L2 * cos(self.theta2),
        )


def main():
    t1 = time.time()

    pendulum = DIPC()
    for _ in range(10):
        pendulum.update()

    print(pendulum.sols)
    print(f"w0: {pendulum.w0}, w1: {pendulum.w1}, w2: {pendulum.w2}")
    print(
        f"theta0: {pendulum.theta0}, theta1: {pendulum.theta1}, theta2: {pendulum.theta2}"
    )

    t2 = time.time()

    print(t2 - t1)


if __name__ == "__main__":
    main()
