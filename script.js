let xmlHttpRequest = new XMLHttpRequest();
xmlHttpRequest.open(
  'GET',
  'http://127.0.0.1:8000/hives/states/',
  true
);
xmlHttpRequest.send();

xmlHttpRequest.onreadystatechange = function() {
  if (xmlHttpRequest.readyState != 4) {
    return
  }

  if (xmlHttpRequest.status === 200) {
    console.log('result', xmlHttpRequest.responseText)
  } else {
    console.log('err', xmlHttpRequest.responseText)
  }
}

let response = await fetch();

if (response.ok) { // если HTTP-статус в диапазоне 200-299
  // получаем тело ответа (см. про этот метод ниже)
  let json = await response.json();
} else {
  alert("Ошибка HTTP: " + response.status);
}