let interval;

function generate(e) {
  if (e) e.preventDefault();
  const qs = (v) => document.querySelector(v);
  const amountOfNumbers = parseInt(qs('#max-numbers').value, 10);
  const amountToSelect = parseInt(qs('#numbers-to-pick').value, 10);
  const numbersContainer = qs('.numbers');
  const allNumbers = [];
  let created = 0;
  if (isNaN(amountOfNumbers)
      || isNaN(amountToSelect)
      || amountOfNumbers <= 0
      || amountToSelect <= 0
      || amountToSelect > amountOfNumbers) return;

  clearInterval(interval);

  while (numbersContainer.lastChild) {
    numbersContainer.removeChild(numbersContainer.lastChild);
  }
  qs('#result-row').classList.remove('max-opacity');
  // qs('#results').innerText = '';

  interval = setInterval(() => {
    if (created < amountOfNumbers) {
      if (created > 0) {
        numbersContainer.lastChild.classList.remove('init');
      }
      const element = document.createElement('div');
      const number = created + 1;
      element.innerHTML = number;
      element.className = 'nr init';
      numbersContainer.appendChild(element);
      created += 1;
      allNumbers.push({ element, number });
    } else {
      numbersContainer.lastChild.classList.remove('init');
      clearInterval(interval);
      const winningNumbers = [];
      const tmp = [...allNumbers];
      for (let i = 0; i < amountToSelect; i++) {
        const idx = Math.floor(Math.random() * tmp.length);
        tmp[idx].element.classList.add('active');
        winningNumbers.push(tmp.splice(idx, 1)[0]);

      }
      // qs('#result-row').style.opacity = '1';
      qs('#result-row').classList.add('max-opacity');
      qs('#results').innerText = winningNumbers
        .map(nr => nr.number)
        .sort((a, b) => a - b)
        .join(', ');
    }
  }, 40)
}

generate();
