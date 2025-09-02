// In-place quicksort implementation (iterative stack-based partitioning)

function quicksort(arr, compare) {
  if (!Array.isArray(arr)) throw new TypeError('arr must be an array');
  if (arr.length <= 1) return arr;

  const cmp = typeof compare === 'function' ? compare : (a, b) => a - b;

  function partition(a, low, high) {
    const pivot = a[high];
    let i = low - 1;
    for (let j = low; j < high; j++) {
      if (cmp(a[j], pivot) <= 0) {
        i++;
        [a[i], a[j]] = [a[j], a[i]];
      }
    }
    [a[i + 1], a[high]] = [a[high], a[i + 1]];
    return i + 1;
  }

  const stack = [];
  stack.push(0, arr.length - 1);

  while (stack.length) {
    const high = stack.pop();
    const low = stack.pop();
    if (low < high) {
      const p = partition(arr, low, high);
      // Push subarrays to stack; process smaller first to limit stack size
      if (p - 1 - low > high - (p + 1)) {
        stack.push(low, p - 1);
        stack.push(p + 1, high);
      } else {
        stack.push(p + 1, high);
        stack.push(low, p - 1);
      }
    }
  }

  return arr;
}

module.exports = { quicksort };
