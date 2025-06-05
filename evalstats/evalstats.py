#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import numpy as np
from concurrent.futures import ThreadPoolExecutor

__author__ = ['Nico Curti']
__email__ = ['nico.curti2@unibo.it']

class EvalStats:
  '''
  A class to compute statistics asynchronously using NumPy.
  This class uses a thread pool executor to run NumPy operations in parallel,
  which is useful for CPU-bound tasks like statistical computations.

  Parameters
  ----------
  data : list or np.ndarray
    The input data for which statistics will be computed. It should be a
    one-dimensional array-like structure.

  num_workers : int, optional (default=4)
    The number of worker threads to use for parallel computation. Default is 4.
  '''
  def __init__(self, data : list, num_workers : int = 4):
    # Validate input data
    self._data = np.asarray(data)
    
    # convert to a one-dimensional array
    self._data = self._data.flatten()

    # set the number of workers
    if not isinstance(num_workers, int) or num_workers <= 0:
      raise ValueError(f'num_workers must be a positive integer')
    self._num_workers = num_workers

  def __getattr__(self, name):
    '''
    Dynamically retrieve statistics methods based on the attribute name.
    
    Parameters
    ----------
    name : str
      The name of the attribute to retrieve. It should match one of the
      statistics methods (e.g., 'mean', 'std', 'min', 'max', 'count', 'sum',
      'variance').
    
    Returns
    -------
    float or int
      The computed statistic corresponding to the attribute name.
    
    Raises
    -------
    AttributeError
      If the attribute name does not match any of the statistics methods.
    '''
    # Dynamically create methods for computing statistics
    if not hasattr(self, f'compute_{name}'):
      raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    # check if the method exists in the class
    if name not in self.__dict__:
      # call the method to compute the statistic
      self.__dict__[name] = eval(f'self.compute_{name}()')
    # return the value of the attribute
    return self.__dict__[name]
  
  def update_data(self, new_data : list):
    '''
    Update the data with new values.

    Parameters
    ----------
    new_data : list
      A list of new data points to update the existing data.
    '''
    # Convert new_data to a numpy array and flatten it
    self._data = np.asarray(new_data).flatten()
    # clear the cached statistics
    self.__dict__ = {
      k: v 
      for k, v in self.__dict__.items() 
      if k.startswith('_')
    }
    return self

  def compute_mean(self) -> float:
    '''
    Compute the mean of the data.

    Returns
    -------
    float
      The mean of the data.
    '''
    return np.mean(self._data)
  
  def compute_std(self) -> float:
    '''
    Compute the standard deviation of the data.

    Returns
    -------
    float
      The standard deviation of the data.
    '''
    return np.std(self._data)
  
  def compute_min(self) -> float:
    '''
    Compute the minimum value of the data.

    Returns
    -------
    float
      The minimum value of the data.
    '''
    return np.min(self._data)
  
  def compute_max(self) -> float:
    '''
    Compute the maximum value of the data.

    Returns
    -------
    float
      The maximum value of the data.
    '''
    return np.max(self._data)
  
  def compute_count(self) -> int:
    '''
    Compute the count of the data.

    Returns
    -------
    int
      The number of elements in the data.
    '''
    return len(self._data)
  
  def compute_sum(self) -> float:
    '''
    Compute the sum of the data.

    Returns
    -------
    float
      The sum of the data.
    '''
    return np.sum(self._data)
  
  def compute_variance(self) -> float:
    '''
    Compute the variance of the data.

    Returns
    -------
    float
      The variance of the data.
    '''
    return np.var(self._data)
  
  def compute_all(self) -> dict:
    '''
    Compute all statistics and return them as a dictionary.

    Returns
    -------
    dict
      A dictionary containing the mean, standard deviation, minimum,
      maximum, total sum, and variance of the data.
    '''

    def _block(x_block : np.ndarray) -> tuple:
      '''
      Compute statistics for a block of data.

      Parameters
      ----------
      x_block : np.ndarray
        A block of data to compute statistics on.
      Returns
      -------
      tuple
        A tuple containing the mean, sum of squares, minimum, and maximum
        of the block.
      '''
      mu = np.sum(x_block)
      mu2 = np.sum(x_block ** 2)
      m = np.min(x_block)
      M = np.max(x_block)
      return mu, mu2, m, M
    
    async def _async_parallel(x : np.ndarray, num_threads : int=4) -> tuple:
      '''
      Asynchronously compute statistics in parallel using a thread pool.
      
      Parameters
      ----------
      x : np.ndarray
        The input data to compute statistics on.
      num_threads : int, optional (default=4)
        The number of threads to use for parallel computation.
      
      Returns
      -------
      tuple
        A tuple containing the mean, standard deviation, minimum, maximum,
        total sum, and variance of the input data.
      '''
      # Split the data into blocks for parallel processing
      n = len(x)
      # If the number of threads is greater than the data length, use the data length
      if num_threads > n:
        num_threads = n
      # Calculate the block size and create blocks
      block_size = (n + num_threads - 1) // num_threads
      # Create blocks of data
      blocks = [
        x[i:i + block_size] 
        for i in range(0, n, block_size)
      ]

      # Define the event loop and executor for parallel execution
      loop = asyncio.get_running_loop()
      # Use ThreadPoolExecutor to run the blocking function in parallel
      with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create a list of async tasks for each block
        tasks = []
        for block in blocks:
          # Submit eval_block to executor, wrapped in async future
          task = loop.run_in_executor(executor, _block, block)
          tasks.append(task)
        # Gather results from all tasks
        results = await asyncio.gather(*tasks)
      
      # Combine results from all blocks
      total_mu = sum(r[0] for r in results)
      total_mu2 = sum(r[1] for r in results)
      global_min = min(r[2] for r in results)
      global_max = max(r[3] for r in results)
      # Calculate the mean and variance
      mu = total_mu / n
      var = (total_mu2 / n - mu * mu)
      # Return the computed statistics
      return mu, var ** 0.5, global_min, global_max, total_mu, var
    
    # Run the async function to compute statistics
    if not asyncio.get_event_loop().is_running():
      # If no event loop is running, create a new one
      asyncio.set_event_loop(asyncio.new_event_loop())

    # Call the async function to compute statistics
    stats = asyncio.run(
      _async_parallel(
        x=self._data, 
        num_threads=self._num_workers
      )
    )

    # Return the statistics as a dictionary
    return {
      'mean': stats[0],
      'std': stats[1],
      'min': stats[2],
      'max': stats[3],
      'count': len(self._data),
      'sum': stats[4],
      'variance': stats[5],
    }
  
  def __repr__(self):
    return f"EvalStats(data={self._data}, num_workers={self._num_workers})"
  
  def __str__(self):
    return f"EvalStats with {len(self._data)} elements and {self._num_workers} workers"
  