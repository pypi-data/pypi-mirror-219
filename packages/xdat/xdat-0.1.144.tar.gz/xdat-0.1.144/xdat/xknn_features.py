"""
Use nearest neighbors to extract new features

Target unrelated features:
- Min, mean, median, max of neighborhood
- z-score of sample within neighborhood (how "normal" the value is)
- Number of samples in neighborhood (if distance given) // Neighborhood size (if samples given)

Target related features:
- KNN prediction (by feature)
- Ideal neighborhood size?
"""