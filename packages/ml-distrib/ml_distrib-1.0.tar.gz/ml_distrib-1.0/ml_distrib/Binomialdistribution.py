import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials

    TODO: Fill out all TODOs in the functions below
    """
    #       A binomial distribution is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    #

    def __init__(self, prob=.5, size=20):

        # TODO: store the probability of the distribution in an instance variable p
        # TODO: store the size of the distribution in an instance variable n

        # TODO: Now that you know p and n, you can calculate the mean and standard deviation
        #       Use the calculate_mean() and calculate_stdev() methods to calculate the
        #       distribution mean and standard deviation
        #
        #       Then use the init function from the Distribution class to initialize the
        #       mean and the standard deviation of the distribution
        #
        #       Hint: You need to define the calculate_mean() and calculate_stdev() methods
        #               farther down in the code starting in line 55.
        #               The init function can get access to these methods via the self
        #               variable.
        self.p = prob
        self.n = size
        self.data = []

        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())


    def calculate_mean(self):
        self.mean = self.p * self.n

        return self.mean

    def calculate_stdev(self):
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value
        """
        self.p = 1.0 * sum(self.data) / len(self.data)
        self.n =  len(self.data)
        self.stdev = self.calculate_stdev()
        self.mean = self.calculate_mean()

        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

        # TODO: Use the matplotlib package to plot a bar chart of the data
        #       The x-axis should have the value zero or one
        #       The y-axis should have the count of results for each case
        #
        #       For example, say you have a coin where heads = 1 and tails = 0.
        #       If you flipped a coin 35 times, and the coin landed on
        #       heads 20 times and tails 15 times, the bar chart would have two bars:
        #       0 on the x-axis and 15 on the y-axis
        #       1 on the x-axis and 20 on the y-axis

        #       Make sure to label the chart with a title, x-axis label and y-axis label
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')

    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.

        Args:
            k (float): point for calculating the probability density function

        Returns:
            float: probability density function output
        """

        binomial_coefficient = math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k)))
        p_of_successes_and_failures = (self.p ** k) * (1 - self.p) ** (self.n - k)
        
        return binomial_coefficient * p_of_successes_and_failures 

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y

    def __add__(self, other):

        """Function to add together two Binomial distributions with equal p
        Args:
            other (Binomial): Binomial instance
        Returns:
            Binomial: Binomial distribution
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        res = Binomial()
        res.n = self.n + other.n
        res.p = self.p
        res.calculate_stdev()
        res.calculate_mean()
        
        return res

    def __repr__(self):

        """Function to output the characteristics of the Binomial instance
        Args:
            None
        Returns:
            string: characteristics of the Gaussian
        """

        # TODO: Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20
        #
        #       with the values replaced by whatever the actual distributions values are
        #       The method should return a string in the expected format
        return "mean {}, standard deviation {}, p {}, n {}".\
        format(self.mean, self.stdev, self.p, self.n)

