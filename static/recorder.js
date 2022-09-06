const buttonRecord = document.getElementById("record");
const buttonStop = document.getElementById("stop");
const downloadLink = document.getElementById("download");
const link = document.getElementById("download");
const messageEl = document.getElementById("message");

buttonStop.disabled = true;
downloadLink.hidden = true;
messageEl.hidden = true;

buttonRecord.onclick = function () {
  // var url = window.location.href + "record_status";
  buttonRecord.disabled = true;
  buttonStop.disabled = false;
  messageEl.hidden = false;

  // disable download link
  downloadLink.hidden = true;

  // XMLHttpRequest
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // alert(xhr.responseText);
    }
  };
  xhr.open("POST", "/record_status");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify({ status: "true" }));
};

buttonStop.onclick = function () {
  buttonRecord.disabled = false;
  buttonStop.disabled = true;
  messageEl.hidden = true;

  // XMLHttpRequest
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // alert(xhr.responseText);

      // enable download link
      downloadLink.hidden = false;
      downloadLink.href = "/static/video.avi";
    }
  };
  xhr.open("POST", "/record_status");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify({ status: "false" }));
};
