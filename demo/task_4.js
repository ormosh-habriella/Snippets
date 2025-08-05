const fruits = ["apple", "banana"];

function createObjectFromKeys(fruits) {
  let result = {};
  for (let fruit of fruits) {
      result[fruit] = fruit.length;
  }
  return result;
}

console.log(createObjectFromKeys(fruits));
// Ожидаемый результат: { apple: 5, banana: 6 }