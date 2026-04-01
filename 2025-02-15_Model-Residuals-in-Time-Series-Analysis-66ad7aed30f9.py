# Description: Short example for Model Residuals in Time Series Analysis.



from scipy import stats
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import acf  # Correct import
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)




class ResidualAnalyzer:
    """
    A toolkit for analyzing residuals.
    """
    def __init__(self, actual_values, predicted_values):
        self.actual = np.array(actual_values)
        self.predicted = np.array(predicted_values)
        self.residuals = self.actual - self.predicted

    def basic_statistics(self):
        """
        Get key stats on residuals.
        """
        stats_dict = {
            'Mean': np.mean(self.residuals),
            'Std Dev': np.std(self.residuals),
            'Skewness': stats.skew(self.residuals),
            'Kurtosis': stats.kurtosis(self.residuals),
            'Min': np.min(self.residuals),
            'Max': np.max(self.residuals)
        }
        return pd.Series(stats_dict)

    def plot_residual_distribution(self):
        """
        Show how residuals are distributed.
        """
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        sns.histplot(self.residuals, kde=True)
        plt.title('Residual Distribution')
        plt.xlabel('Residual Value')
        plt.ylabel('Frequency')
        plt.savefig("residual_distribution.png")
        
        plt.subplot(1, 2, 2)
        stats.probplot(self.residuals, dist="norm", plot=plt)
        plt.title('Q-Q Plot of Residuals')
        plt.savefig("qq_plot.png")
        
        plt.tight_layout()
        plt.show()

    def normality_tests(self):
        """
        Run normality tests on residuals.
        """
        shapiro_stat, shapiro_p = stats.shapiro(self.residuals)
        anderson_result = stats.anderson(self.residuals)
        jb_stat, jb_p = stats.jarque_bera(self.residuals)

        results = {
            'Shapiro-Wilk': {'statistic': shapiro_stat, 'p-value': shapiro_p},
            'Anderson-Darling': {'statistic': anderson_result.statistic, 
                                 'critical_values': anderson_result.critical_values},
            'Jarque-Bera': {'statistic': jb_stat, 'p-value': jb_p}
        }
        return results

    def autocorrelation_analysis(self, nlags=40):
        """
        Check if residuals are autocorrelated.
        """
        acf_values = acf(self.residuals, nlags=nlags, fft=False)
        confidence_interval = 1.96 / np.sqrt(len(self.residuals))
        
        plt.figure(figsize=(12, 4))
        plt.bar(range(len(acf_values)), acf_values)
        plt.axhline(y=confidence_interval, color='r', linestyle='--')
        plt.axhline(y=-confidence_interval, color='r', linestyle='--')
        plt.title('Autocorrelation Function of Residuals')
        plt.xlabel('Lag')
        plt.ylabel('ACF')
        plt.savefig("autocorrelation_function.png")
        
        plt.show()
        return acf_values

    def interpret_residual_analysis(self):
        """
        Explain what the residuals tell us.
        """
        interpretations = []
        stats = self.basic_statistics()
        if abs(stats['Mean']) < 0.1:
            interpretations.append("Residuals have a near-zero mean, which is good.")
        else:
            interpretations.append("Residuals show bias, suggesting model adjustments are needed.")
        
        normality_tests = self.normality_tests()
        shapiro_p = normality_tests['Shapiro-Wilk']['p-value']
        if shapiro_p > 0.05:
            interpretations.append("Residuals look normally distributed.")
        else:
            interpretations.append("Residuals deviate from normality, which may impact reliability.")
        
        return "\n".join(interpretations)

def main():
    """
    Main function to demonstrate the ResidualAnalyzer
    """
    # Example dataset (simulated)
    np.random.seed(42)
    actual_values = np.random.normal(loc=50, scale=10, size=100)
    predicted_values = actual_values + np.random.normal(loc=0, scale=5, size=100)

    # Initialize ResidualAnalyzer
    analyzer = ResidualAnalyzer(actual_values, predicted_values)
    
    # Print basic statistics
    logger.info("### Basic Statistics ###")
    logger.info(analyzer.basic_statistics())

    # Plot residual distribution
    logger.info("\n### Residual Distribution ###")
    analyzer.plot_residual_distribution()

    # Perform normality tests
    logger.info("\n### Normality Tests ###")
    normality_results = analyzer.normality_tests()
    for test, result in normality_results.items():
        logger.info(f"{test}: {result}")

    # Perform autocorrelation analysis
    logger.info("\n### Autocorrelation Analysis ###")
    analyzer.autocorrelation_analysis(nlags=20)

    # Interpret residual analysis
    logger.info("\n### Residual Analysis Interpretation ###")
    logger.info(analyzer.interpret_residual_analysis())

if __name__ == "__main__":
    main()

### Normality Tests ###
Shapiro-Wilk: {'statistic': 0.977533993395285, 'p-value': 0.0852560281344462}
Anderson-Darling: {'statistic': 0.6214102099727086, 'critical_values': array([0.555, 0.632, 0.759, 0.885, 1.053])}
Jarque-Bera: {'statistic': 2.42505305943258, 'p-value': 0.29744482609021683}
