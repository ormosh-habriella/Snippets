const data = { a: 1, b: 2, c: 3 };

function sumObjectValues(object) {
  let sum = 0;
  for (let value of Object.values(object)) {
      sum += value;
  }
  return sum;
}

console.log(sumObjectValues(data));