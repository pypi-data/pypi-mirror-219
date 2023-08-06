class Distribution():
    def __init__(self, mu = 0, sigma = 1):
        self.mean = mu
        self.stdev = sigma
        self.data = []

    def read_data_file(self, file_name, sample=True):
        """Method to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.
        After reading in the file, the mean and standard deviation are calculated

        Args:
            file_name (string): name of a file to read from
        Returns:
            None
        """
        # This code opens a data file and appends the data to a list called data_list
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list

    def calculate_mean(self):
        """Method to calculate the mean of the data set.
        Args:
            None
        Returns:
            float: mean of the data set
        """
        self.mean = 1.0 * sum(self.data) / len(self.data)
        return self.mean

    def calculate_stdev(self, sample=True):

        """Method to calculate the standard deviation of the data set.
        Args:
            sample (bool): whether the data represents a sample or population
        Returns:
            float: standard deviation of the data set
        """

        mean = self.mean
        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)
        sigma = 0
        sigma = sum((x_i - self.mean) ** 2 for x_i in self.data)
        self.stdev = math.sqrt(sigma / n)
        return self.stdev
