const btnUp = document.getElementById("btnUp");
const btnDown = document.getElementById("btnDown");
const btnLeft = document.getElementById("btnLeft");
const btnRight = document.getElementById("btnRight");
const btnStop = document.getElementById("btnStop");
const buttons = [btnUp, btnDown, btnLeft, btnRight];

function handleClick(option) {
  let data = {
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

btnUp.addEventListener("pointerdown", () => {
  handleClick("up");
});

btnDown.addEventListener("pointerdown", () => {
  handleClick("down");
});

btnLeft.addEventListener("pointerdown", () => {
  handleClick("left");
});

btnRight.addEventListener("pointerdown", () => {
  handleClick("right");
});

btnStop.addEventListener("pointerdown", () => {
  handleClick("off");
});

buttons.forEach((btn) => {
  btn.addEventListener("pointerup", () => {
    handleClick("off");
  });
});
