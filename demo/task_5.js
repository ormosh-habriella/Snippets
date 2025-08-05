function findDuplicates(array) {
    let numbersObject = {};
    for (let num of array) {
        numbersObject[num] = console.count(num);
    }
}

const numbers = [1, 2, 3, 4, 2, 5, 1];
console.log(findDuplicates(numbers)); // [1, 2]