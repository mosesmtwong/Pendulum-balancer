import sympy as smp
import time
from math import sin, cos, pi


class DIPC:
    def __init__(
        self,
        g=10,
        u=0,
        m0=20,
        m1=5,
        m2=5,
        L1=1,
        L2=1,
        h=0.5,
        w=1,
        theta0=0,
        theta1=pi / 4,
        theta2=0,
        w0=0,
        w1=0,
        w2=0,
        dt=0.01,
    ):
        self.dt = dt
        self.h, self.w = (h, w)
        self.g, self.u = (g, u)
        self.half = smp.Rational(1, 2)
        self.m0, self.m1, self.m2 = (m0, m1, m2)
        self.L1, self.L2 = (L1, L2)
        self.l1, self.l2 = (L1 / 2, L2 / 2)
        self.I1, self.I2 = (m1 * L1**2 / 12, m2 * L2**2 / 12)
        self.theta0, self.theta1, self.theta2 = (theta0, theta1, theta2)
        self.w0, self.w1, self.w2 = (w0, w1, w2)
        self.a0, self.a1, self.a2 = smp.symbols(
            "\u03B8\u0308_0 \u03B8\u0308_1 \u03B8\u0308_2"
        )

    def update(self):

        m1l1m2L1 = self.m1 * self.l1 + self.m2 * self.L1

        self.expr0 = (
            (self.m0 + self.m1 + self.m2) * self.a0
            + m1l1m2L1 * smp.cos(self.theta1) * self.a1
            + self.m2 * self.l2 * smp.cos(self.theta2) * self.a2
            - m1l1m2L1 * smp.sin(self.theta1) * self.w1**2
            - self.m2 * self.l2 * smp.sin(self.theta2) * self.w2**2
            - self.u
        )
        self.expr1 = (
            m1l1m2L1 * smp.cos(self.theta1) * self.a0
            + (self.m2 * self.l1**2 + self.m2 * self.L1**2 + self.I1) * self.a1
            + self.m2 * self.L1 * self.l2 * smp.cos(self.theta1 - self.theta2) * self.a2
            + self.m2
            * self.L1
            * self.l2
            * smp.sin(self.theta1 - self.theta2)
            * self.w2**2
            - m1l1m2L1 * self.g * smp.sin(self.theta1)
        )
        self.expr2 = (
            self.m2 * self.l2 * smp.cos(self.theta2) * self.a0
            + self.m2 * self.L1 * self.l2 * smp.cos(self.theta1 - self.theta2) * self.a1
            + (self.m2 * self.l2**2 + self.I2) * self.a2
            - self.m2
            * self.L1
            * self.l2
            * smp.sin(self.theta1 - self.theta2)
            * self.w1**2
            - self.m2 * self.l2 * self.g * smp.sin(self.theta2)
        )

        self.sols = smp.solve(
            [self.expr0, self.expr1, self.expr2], [self.a0, self.a1, self.a2]
        )

        self.w0 += self.sols[self.a0] * self.dt
        self.w1 += self.sols[self.a1] * self.dt
        self.w2 += self.sols[self.a2] * self.dt

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
