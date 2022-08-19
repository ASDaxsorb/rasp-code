const btnUp = document.getElementById("btnUp");
const btnDown = document.getElementById("btnDown");
const btnLeft = document.getElementById("btnLeft");
const btnRight = document.getElementById("btnRight");
const btnStop = document.getElementById("btnStop");

const buttons = [btnUp, btnDown, btnLeft, btnRight];

function handleClick(option) {
  data = {
    direction: option.trim().toLowerCase(),
  };

  fetch("/move", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((resp) => console.log(resp));
}

btnUp.addEventListener("mousedown", () => {
  handleClick("up");
});

btnDown.addEventListener("mousedown", () => {
  handleClick("down");
});

btnLeft.addEventListener("mousedown", () => {
  handleClick("left");
});

btnRight.addEventListener("mousedown", () => {
  handleClick("right");
});

btnStop.addEventListener("mousedown", () => {
  handleClick("off");
});

buttons.forEach((btn) => {
  btn.addEventListener("mouseup", () => {
    handleClick("off");
  });
});
