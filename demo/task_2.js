function countVowels(string) {
  const vowels = "aeiou";
  let count_vowels = 0;
  for (let letter of string) {
      if (vowels.includes(letter)) {
          count_vowels++;
      }
    }
  return count_vowels;
}

console.log(countVowels("hello world"))