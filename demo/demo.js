let cost = Number(prompt("Стоимость товара:"));
let n = Number(prompt("Количество товаров:"));

// let number = 1
//
// while (number <= n) {
//     console.log(`Количество: ${number} цена: ${number * cost}`);
//     number++;
//
// }

for (let number = 1; number <= n; number++) {
    console.log(`Количество: ${number} цена: ${number * cost}`);
}