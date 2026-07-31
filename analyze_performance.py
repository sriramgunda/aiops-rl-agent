from src.analysis.performance_analyzer import PerformanceAnalyzer

if __name__ == "__main__":
    analyzer = PerformanceAnalyzer(
        performance_file="results/performance_report.json",
        evaluation_file="results/evaluation_summary.json",
        output_dir="results/performance"
    )

    print("=" * 60)
    print("AIOps Performance Analysis")
    print("=" * 60)

    analyzer.generate()

    print("=" * 60)
    print("Analysis reports saved to results/performance/")
    print("=" * 60)

    print("Performance analysis completed successfully.")