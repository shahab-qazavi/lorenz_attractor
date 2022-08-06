import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
from exception import DetailException


class LorenzAttractor:
    def __init__(self):
        self.N_trajectories = 20
        self.lines = None
        self.pts = None
        self.x_t = None
        self.fig = plt.figure()
        self.ax = None
        self.anim = None
        self.rho = 28.0
        self.beta = 8. / 3
        self.sigma = 10.
        plt.style.use('dark_background')

    def lorentz_derivative(self, xyz, t0):
        # Compute the time-derivative of a Lorentz system
        x, y, z = xyz
        return [self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z]

    # Choose random starting points, uniformly distributed from -15 to 15
    def prepare_var(self):
        try:
            np.random.seed(1)
            x0 = -15 + 30 * np.random.random((self.N_trajectories, 3))

            # Solve for the trajectories
            t = np.linspace(0, 10, 5000)
            self.x_t = np.asarray([integrate.odeint(self.lorentz_derivative, x0i, t)
                                   for x0i in x0])

            # Set up figure & 3D axis for animation

            self.ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
            self.ax.axis('off')

            # choose a different color for each trajectory
            colors = plt.cm.jet(np.linspace(0, 1, self.N_trajectories))

            # set up lines and points
            self.lines = sum([self.ax.plot([], [], [], '-', c=c)
                              for c in colors], [])
            self.pts = sum([self.ax.plot([], [], [], 'o', c=c)
                            for c in colors], [])

            # prepare the axes limits
            self.ax.set_xlim((-25, 25))
            self.ax.set_ylim((-35, 35))
            self.ax.set_zlim((5, 55))

            # set point-of-view: specified by (altitude degrees, azimuth degrees)
            self.ax.view_init(30, 0)
        except:
            raise ValueError(f'{DetailException.get_exception_details()}')

    # initialization function: plot the background of each frame
    def init(self):
        try:
            for line, pt in zip(self.lines, self.pts):
                line.set_data([], [])
                line.set_3d_properties([])

                pt.set_data([], [])
                pt.set_3d_properties([])
            return self.lines + self.pts
        except:
            raise AssertionError(f'{DetailException.get_exception_details()}')

    # animation function.  This will be called sequentially with the frame number
    def animate(self, i):
        try:
            # we'll step two time-steps per frame.  This leads to nice results.
            i = (5 * i) % self.x_t.shape[1]

            for line, pt, xi in zip(self.lines, self.pts, self.x_t):
                x, y, z = xi[:i].T
                line.set_data(x, y)
                line.set_3d_properties(z)

                # pt.set_data(x[-1:], y[-1:])
                # pt.set_3d_properties(z[-1:])

            self.ax.view_init(30, 0.3 * i)
            self.fig.canvas.draw()
            return self.lines + self.pts
        except:
            raise AssertionError(f'{DetailException.get_exception_details()}')

    def prepare_animating(self):
        self.prepare_var()

        # instantiate the animator.
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                            frames=2000, interval=30, blit=True)

    def save_file(self):
        self.prepare_animating()
        # Save as mp4. This requires mplayer or ffmpeg to be installed
        try:
            self.anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
        except:
            raise AssertionError(f'{DetailException.get_exception_details()}')

    def draw(self):
        self.prepare_animating()
        try:
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            plt.show()
        except:
            raise AssertionError(f'{DetailException.get_exception_details()}')


if __name__ == '__main__':

    obj = LorenzAttractor()
    obj.draw()


