const optLength = document.getElementById("size").options.length;
for (i = 0; i < optLength; i++) {
  if (document.getElementById("size").options[i].value == itemId) {
    document.getElementById("size").options[i].selected = "selected";
    if (parseInt(stock) > 1) {
      document.getElementById("stock").innerHTML = `${stock} items in stock`;
    } else if (parseInt(stock) == 1) {
      document.getElementById("stock").innerHTML = `${stock} item in stock`;
    } else {
      document.getElementById("stock").innerHTML = "Out of stock";
      document.getElementById("stock").style.color = "lightcoral";
    }
    break;
  }
}

function changeStock(opt) {
  let size = opt.options[opt.selectedIndex].value;
  if ((size != 0) & (size != itemId)) {
    location.href = defaultProductURL.replace("0/", size);
  }
}

function titleCase(txt) {
  let text = txt.split("-");
  for (var i = 0; i < text.length; i++) {
    text[i] = text[i].charAt(0).toUpperCase() + text[i].slice(1);
  }
  text = text.join(" ");
  return text;
}

const element = document.querySelectorAll(".item-color");
element.forEach((e) => {
  e.addEventListener("mouseenter", function checkHover() {
    const text = titleCase(e.id);
    document.getElementById(
      "text-color"
    ).innerHTML = `<strong>Color: </strong>${text}`;
    document.getElementById("img-item").src =
      e.getElementsByTagName("img")[0].src;
  });
  e.addEventListener("mouseleave", function checkHover() {
    document.getElementById("text-color").innerHTML = defaultColor;
    document.getElementById("img-item").src = defaultImg;
  });
});

const qtyElement = document.getElementById("qty");
const maxKeyCode = 49 + parseInt(stock);
qtyElement.onkeydown = function (e) {
  let quantity = parseInt(qtyElement.value);
  if (e.keyCode == 8) {
    return true;
  } else if (
    e.keyCode < 49 ||
    e.keyCode >= maxKeyCode ||
    parseInt(String.fromCharCode(e.keyCode)) + quantity > quantity
  ) {
    return false;
  }
};

function addToCart() {
  const quantity = document.getElementById("qty").value;
  let url = defaultAddToCartURL.replace(/0/, quantity);
  location.href = url;
}
