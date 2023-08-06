import random

def initialise_weights(structure, inputs):
  weights = []
  together = [inputs] + structure
  # For each layer
  for i in range(len(structure)):
    weights.append([])
    # For each node in the layer
    for y in range(structure[i]):
      weights[i].append([])
      # For each weight leading up to the node (From each of the previous layer)
      for j in range(together[i]):
        weights[i][y].append(random.uniform(-1,1))
  return weights

def initialise_weights_zeros(structure, inputs):
  weights = []
  together = [inputs] + structure
  # For each layer
  for i in range(len(structure)):
    weights.append([])
    # For each node in the layer
    for y in range(structure[i]):
      weights[i].append([])
      # For each weight leading up to the node (From each of the previous layer)
      for j in range(together[i]):
        weights[i][y].append(0)
  return weights

def initialise_weights_zeros_multioutput(structure, inputs, outputs):
  weights = []
  together = [inputs] + structure
  # For each layer
  for i in range(len(structure)):
    weights.append([])
    # For each node in the layer
    for y in range(structure[i]):
      weights[i].append([])
      # For each weight leading up to the node (From each of the previous layer)
      for j in range(together[i]):
        weights[i][y].append([])
        # For each output node that the weight affects
        for o in range(outputs):
          weights[i][y][j].append(0)
  return weights

def summation(weights, inputs):
  total = 0
  for i in range(len(inputs)):
    total = total + (weights[i] * inputs[i])
  return total

def logisticCell(weights, inputs):
    total = summation(weights, inputs)
    return 1 / (1 + pow(2.71828, total))

def binaryStepCell(weights, inputs):
  total = summation(weights, inputs)
  if (total < 0):
    output = 0
  else:
    output = 1
  return output

def linearCell(weights, inputs):
  return summation(weights, inputs)

def tanhCell(weights, inputs):
  e = 2.718281828459045235360
  total = summation(weights, inputs)
  print("Tanh total:", total)
  return (pow(e, total) - pow(e, -total)) / (pow(e, total) + pow(e, -total))

def reluCell(weights, inputs):
  total = summation(weights, inputs)
  return max(0, total)

def runLayer(weights, inputs, nodes, type):
    outputs = []
    for i in range(nodes):
      #["relu", "logistic", "linear", "tanh", "relu", "logistic", "linear", "tanh", "relu", "logistic"]
      if (type == "logistic"):
        outputs.append(logisticCell(weights[i], inputs))
      elif (type == "relu"):
        outputs.append(reluCell(weights[i], inputs))
      elif (type == "linear"):
        outputs.append(linearCell(weights[i], inputs))
      elif (type == "tanh"):
        outputs.append(tanhCell(weights[i], inputs))
      elif (type == "binary"):
        outputs.append(binaryStepCell(weights[i], inputs))
      else:
        raise ValueError('Unknown cell type given.')
    return outputs

def runNetwork(inputs, weights, nodes, types):
  if (len(nodes) != len(types)):
    raise ValueError('Length of network structure array given does not equal length of node types array.')
  hiddenOutputs = [inputs]
  for i in range (len(nodes) - 1):
    hiddenOutputs.append(runLayer(weights[i], hiddenOutputs[-1], nodes[i], types[i]))
  finalOutputs = runLayer(weights[-1], hiddenOutputs[-1], nodes[-1], types[-1])
  return [hiddenOutputs, finalOutputs]

def loss(t, z, n):
    totals = []
    final = 0
    # For each output node
    for m in range(len(z[0])):
      totals.append(0)
      # For each training example
      for i in range(n):
        totals[m] = totals[m] + pow((t[i][m] - z[i][m]), 2)
      totals[m] = totals[m] / n
    # Now average the totals array
    for m in range(len(totals)):
      final = final + totals[m]
    return final / len(totals)

def adjustWeight(learningRate, gradient, currentWeight):
  return currentWeight + (learningRate * gradient)

def deltaZ(z,t):
    return (z - t) * z * (1 - z)
def outputGradient(nodeOutput, targetOutput, hiddenNodeOutput):
  return deltaZ(nodeOutput, targetOutput) * hiddenNodeOutput
def hiddenGradient(nodeOutput, targetOutput, weight, hiddenNodeOutput, earlierNodeOutput):
  result = []
  for n in range(len(nodeOutput)):
    result.append((deltaZ(nodeOutput[n], targetOutput[n]) * weight) * hiddenNodeOutput * (1 - hiddenNodeOutput) * earlierNodeOutput)
  return result

def epoch(trainingDataInputs, trainingDataOutputs, nodes, weights, epoch, learningRate, types):
  modelResults = []
  hiddenResults = []
  # First run the model and get it's loss, for each training example, and add results to an array
  for i in range(len(trainingDataInputs)):
    modelResults.append(runNetwork(trainingDataInputs[i], weights, nodes, types)[1])
    hiddenResults.append(runNetwork(trainingDataInputs[i], weights, nodes, types)[0])
  print("Epoch", epoch, "loss:", loss(trainingDataOutputs, modelResults, len(modelResults)))
  # Work out the partial derivatives for each output layer weight, for each training example, and get the average
  outputGradients = []
  # For each training example
  for j in range(len(trainingDataOutputs)):
    outputGradients.append([])
    # For each output node
    for n in range(nodes[-1]):
      outputGradients[j].append([])
      # For each weight
      for i in range(len(weights[-1][n])):
        outputGradients[j][n].append(outputGradient(modelResults[j][n], trainingDataOutputs[j][n], hiddenResults[-1][-1][i]))
  avgOutputGradients = []
  # Set up the avgOutputGradients array
  # For each node
  for i in range(len(outputGradients[0])):
    avgOutputGradients.append([])
    # For each weight
    for w in range(len(outputGradients[0][i])):
      avgOutputGradients[i].append(0)
  # Now add it all up
  # For each training example's set of gradients
  for i in range(len(outputGradients)):
    # For each node within the training example
    for j in range(len(outputGradients[i])):
      # For each weight leading up to the node
      for w in range(len(outputGradients[i][j])):
        avgOutputGradients[j][w] = avgOutputGradients[j][w] + outputGradients[i][j][w]
  # Now for each weight, divide it by the number of training examples
  # For each output node
  for i in range(len(avgOutputGradients)):
    # For each weight leading up to the node
    for w in range(len(avgOutputGradients[i])):
      # Divide the summed gradients by the # of training examples
      avgOutputGradients[i][j] = avgOutputGradients[i][j] / len(outputGradients)
  # avgOutputGradients is the set of average gradients for each weight in the output layer
  # Now get the gradients for all of the input and hidden layer weights
  hiddenGradients = []
  # For each training example
  for h in range(len(trainingDataOutputs)):
    hiddenGradients.append([])
    # For each layer of the hidden weights (Except for the last layer)
    for i in range(len(weights) - 1):
      hiddenGradients[h].append([])
      # For each node within the layer
      for j in range(len(weights[i])):
        hiddenGradients[h][i].append([])
        # For each weight leading up to the node
        for n in range(len(weights[i][j])):
          # Calculate the partial derivative for this weight, for this training example
          # With: hiddenGradient(nodeOutput, targetOutput, weight, hiddenNodeOutput, earlierNodeOutput)
          thisHiddenGradient = hiddenGradient(modelResults[h], trainingDataOutputs[h], weights[i][j][n], hiddenResults[h][i + 1][n], hiddenResults[h][i][n])
          hiddenGradients[h][i][j].append(thisHiddenGradient)
  # Now average the different hidden gradients from each of the training examples
  # Create a new set of weights of the correct structure, and set all the weights to zero (but not including the last layer)
  avgHiddenGradients = initialise_weights_zeros_multioutput(nodes[:-1], len(trainingDataInputs[0]), nodes[-1])
  # Now add all of the weights from each of the training example's hidden gradients
  # For each training example
  for i in range(len(trainingDataOutputs)):
    # For each layer of the hidden weights
    for j in range(len(avgHiddenGradients)):
      # For each node of the layer
      for n in range(len(avgHiddenGradients[j])):
        # For each weight leading up to the node
        for y in range(len(avgHiddenGradients[j][n])):
          # For each output node that the weight affects
          for o in range(nodes[-1]):
            # Add this weight's gradient from this training example to the average
            avgHiddenGradients[j][n][y][o] = avgHiddenGradients[j][n][y][o] + hiddenGradients[i][j][n][y][o]
  # For each of the weights, divide them by the total number of training examples to get the average
  # For each layer
  for j in range(len(avgHiddenGradients)):
    # For each node in the layer
    for n in range(len(avgHiddenGradients[j])):
      # For each weight leading up to the node
      for y in range(len(avgHiddenGradients[j][n])):
        # For each output node that the weight affects
        for o in range(nodes[-1]):
          # Divide the weight by the number of training examples, and set the new avg weight to be that
          avgHiddenGradients[j][n][y][o] = avgHiddenGradients[j][n][y][o] / len(trainingDataOutputs)

  # Start adjusting the weights
  # Create another new array for the adjusted weights
  newWeights = initialise_weights_zeros(nodes, len(trainingDataInputs[0]))

  # First, for each of the hiddenGradients
  # For each weight, get it's new weight based on the gradient and put it into the newWeights array
  # For each layer
  for l in range(len(avgHiddenGradients)):
    # For each node in the layer
    for n in range(len(avgHiddenGradients[l])):
      # For each weight leading up to the node
      for w in range(len(avgHiddenGradients[l][n])):
        # For each output node that the weight affects
        for o in range(len(avgHiddenGradients[l][n][w])):
          # Adjust the weight and put it into the newWeights array
          newWeights[l][n][w] = adjustWeight(learningRate, avgHiddenGradients[l][n][w][o], weights[l][n][w])
  # And now for each of the outputGradients
  # For each output node
  for n in range(len(avgOutputGradients)):
    # For each weight leading up to the node
    for w in range(len(avgOutputGradients[n])):
      # Adjust the weight
      newWeights[-1][n][w] = adjustWeight(learningRate, avgOutputGradients[n][w], weights[-1][n][w])
  return newWeights

def trainModel(trainingDataInputs, trainingDataOutputs, nodes, epochs, learningRate, types):
  weightsToRun = initialise_weights(nodes, len(trainingDataInputs[0]))
  for i in range(epochs):
    weightsToRun = epoch(trainingDataInputs, trainingDataOutputs, nodes, weightsToRun, i, learningRate, types)
  return weightsToRun