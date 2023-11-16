import math, sequtils, strutils, tables, sets, sugar

proc solveSystem(A: var seq[seq[float]], b: var seq[float]): seq[float] =
  let n = len(A)

  # Forward elimination
  for i in 0..(n-3):
      # Make the diagonal element 1
      var diag_value = A[i][i]
      A[i] = collect(for a in A[i]: a / diag_value)
      b[i] /= diag_value

      # Make the elements below the diagonal 0
      for j in (i + 1)..(n-3):
          var factor = A[j][i]
          A[j] = collect(for (a, b) in zip(A[j], A[i]): a - factor * b)
          b[j] -= factor * b[i]

  # Backward substitution
  var x: seq[float] = newSeq[float](n)
  for i in countdown(n - 4, -1, 1):
      x[i] = b[i]
      for j in countup(i + 1, n-3):
          x[i] -= A[i][j] * x[j]

  return x

proc polynomialRegression(x, y: seq[float], degree: int): seq[float] =
  let n = len(x)
  
  # Create the Vandermonde matrix
  var X = collect(for x_i in x: collect(for d in 0..degree + 1: pow(x_i, d.float)))
  
  # Transpose the matrix
  # n-1 is a hack, shoulda been just n
  var X_T = collect(for i in 0..(degree + 1): collect(for j in 0..(n-1): X[j][i]))
  
  var X_T_X = collect(for row_X_T in X_T: collect(for col_X in X: sum(collect(for _, (a,b) in zip(row_X_T, col_X): a.float * b.float))))
  
  # Add regularization term to the diagonal elements
  
  for i in 0..(n-1):
      X_T_X[i][i] += 1e-15*4

  # Multiply X_T with y
  var X_T_y = collect(for row_X_T in X_T: sum(collect(for (a, b) in zip(row_X_T, y): a * b)))
  
  # Solve the system of linear equations to find the coefficients
  var coefficients = solve_system(X_T_X, X_T_y)
  
  return coefficients

# proc polynomialRegression(x, y: seq[float], degree: int): seq[float] =
  # let n = len(x)

  # # Create the Vandermonde matrix
  # var X: seq[seq[float]] = newSeq[seq[float]](n)
  # for i in 0..<n:
    # X[i] = newSeq[float](degree + 1)
    # for d in 0..degree:
      # X[i][d] = pow(x[i], d.float64)

  # # Transpose the matrix
  # var XT: seq[seq[float]] = newSeq[seq[float]](degree + 1)
  # for i in 0..degree:
    # XT[i] = newSeq[float](n)
    # for j in 0..<n:
      # XT[i][j] = X[j][i]

  # # Multiply XT with X
  # var XTX: seq[seq[float]] = newSeq[seq[float]](degree + 1)
  # for i in 0..degree:
    # XTX[i] = newSeq[float](degree + 1)
    # for j in 0..n:
      # for k in 0..<n:
        # XTX[i][j] += XT[i][k] * X[k][j]

  # # Add regularization term to the diagonal elements
  # for i in 0..degree:
    # XTX[i][i] += 1e-15 * 4

  # # Multiply XT with y
  # var XTy: seq[float] = newSeq[float](degree + 1)
  # for i in 0..degree:
    # for j in 0..<n:
      # XTy[i] += XT[i][j] * y[j]

  # # Solve the system of linear equations to find the coefficients
  # let coefficients = solveSystem(XTX, XTy)

  # return coefficients

proc easeInOutQuad(t: float): float =
  let t = t * 2.0
  if t < 1.0:
    return t * t / 2.0
  else:
    let t = t - 1.0
    return -(t * (t - 2.0) - 1.0) / 2.0

# Generate some sample data
let points = 8
var x = collect(newSeq, for i in 0..<points: i.float64 / (points - 1).float64)
echo x
var y = collect(newSeq, for i in 0..<points: easeInOutQuad(i.float64 / points.float64))
echo y

# Specify the degree of the polynomial
let degree = 8

# Perform polynomial regression
let coefficients = polynomialRegression(x, y, degree)

# Print the coefficients
echo "Coefficients:", coefficients

# Generate points for the polynomial curve
let res = 120.0

var xCurve = collect(newSeq, for i in 0..<int(max(x) * res) - int(min(x) * res) + 1:
                                     i.float64 / (res - 1) + min(x) * res)
echo "getting curve"
var yCurve = collect(for xi in x_curve: sum(collect(for d, c in coefficients: c * pow(xi, d.float))))

echo "got curve"

# Plot the data points and the polynomial curve
# Note: The plotting part is not directly translatable to Nim, as Nim does not have a built-in plotting library like matplotlib.
# You can use external plotting libraries or export data to plot in another tool.