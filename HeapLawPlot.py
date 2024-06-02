import math
import os
from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import pyplot as plt

# Define the base class for the plotting strategy
class PlotStrategy:
    def plot(self, data):
        raise NotImplementedError("Subclasses must implement the plot method.")

    def save_plot(self, filename):
        plot_directory = 'plot'
        if not os.path.exists(plot_directory):
            os.makedirs(plot_directory)
        plt.savefig(f'{plot_directory}/{filename}')
        plt.clf()  # Clear the figure after saving to avoid overlap


class LogLogPlotStrategy(PlotStrategy):
    def get_Beta_and_alpha(self, data):
        log_x = np.log10([pair[0] for pair in data])
        log_y = np.log10([pair[1] for pair in data])

        coefficients = np.polyfit(log_x, log_y, 1)
        beta, log_alpha = coefficients
        return [beta,log_alpha]




    def plot(self, data, name):
        log_x = np.log10([pair[0] for pair in data])
        log_y = np.log10([pair[1] for pair in data])

        # Perform a linear fit to the log-log data.
        coefficients = np.polyfit(log_x, log_y, 1)
        # The slope and intercept from the fit correspond to beta and log(alpha) respectively.
        beta, log_alpha = coefficients
        alpha = 10 ** log_alpha

        # Create a line based on the fit to plot.
        fit_y = np.polyval(coefficients, log_x)

        # Plot the log-log data points and the fitted line.
        plt.scatter(log_x, log_y, label='Log-Log Data Points')
        plt.plot(log_x, fit_y, label=f'Fit: Alpha={alpha:.3f}, Beta={beta:.3f}', color='red')

        plt.xlabel('log10(Total Words)')
        plt.ylabel('log10(Unique Words)')
        plt.title('Log-Log Plot with Linear Fit')
        plt.legend()

        self.save_plot(name)


class SimplePlotStrategy(PlotStrategy):
    def plot(self, data, name):
        x = np.array([pair[0] for pair in data])
        y = np.array([pair[1] for pair in data])

        # Define the power-law function.
        def power_law(x, alpha, beta):
            return alpha * np.power(x, beta)

        # Fit the power-law function to the data.
        params, _ = curve_fit(power_law, x, y, p0=[1, 1])
        alpha, beta = params

        # Plot the data points.
        plt.scatter(x, y, label='Data Points')

        # Plot the fitted curve.
        fit_y = power_law(x, alpha, beta)
        plt.plot(x, fit_y, label=f'Fit: Alpha={alpha:.3f}, Beta={beta:.3f}', color='red')

        plt.xlabel('Total Words')
        plt.ylabel('Unique Words')
        plt.title('Plot with Power-Law Fit')
        plt.legend()

        self.save_plot(name)


class NonLinearLeastSquaresPlotStrategy(PlotStrategy):

    def plot(self, data, name   ):
        ANB =  LogLogPlotStrategy().get_Beta_and_alpha(data)
        n_data = np.array([pair[0] for pair in data], dtype=float)
        Vn_data = np.array([pair[1] for pair in data], dtype=float)
#use the estimate from log log
        # Initial guess for parameters K and beta.
        K_init, beta_init = ANB[0], ANB[1]

        # Perform the Gauss-Newton algorithm to fit Heaps' Law.
        K, beta = self.gauss_newton(n_data, Vn_data, K_init, beta_init)

        # Use the fitted model to compute V for the range of N.
        fit_Vn = heaps_law(n_data, K, beta)

        # Plot the raw data and the fitted curve.
        plt.scatter(n_data, Vn_data, label='Data Points')
        plt.plot(n_data, fit_Vn, label=f'Fit: K={K:.3f}, beta={beta:.3f}', color='red')
        plt.xlabel('Total Words')
        plt.ylabel('Unique Words')
        plt.legend()
        self.save_plot(name)

    def gauss_newton(self, n_data, Vn_data, K_init, beta_init, max_iter=100, tol=1e-6):
        # Gauss-Newton algorithm for fitting Heaps' Law.
        K, beta = K_init, beta_init

        for _ in range(max_iter):
            # Compute residuals and Jacobian at the current estimate.
            r = heaps_law(n_data, K, beta) - Vn_data
            J_K = n_data**beta
            J_beta = K * n_data**beta * np.log(n_data)
            J = np.column_stack((J_K, J_beta))

            # Update the parameters.
            delta = np.linalg.lstsq(J, -r, rcond=None)[0]
            K, beta = K + delta[0], beta + delta[1]

            # Stop if the change is below the tolerance.
            if np.linalg.norm(delta) < tol:
                break

        return K, beta

# Define the Heaps' law function.
def heaps_law(n, K, beta):
    return K * n**beta

# Define the Heaps' law function
def heaps_law(n, K, beta):
    return K * n**beta

# Define the context that uses the strategy
class HeapsLawAnalyzer:
    def __init__(self, strategy=None):
        self.strategy = strategy
        self.data = []

    def set_strategy(self, strategy):
        self.strategy = strategy


    def perform_plot(self,data,name):
        if not self.strategy:
            raise ValueError("Strategy not set")
        self.strategy.plot(data,name)

