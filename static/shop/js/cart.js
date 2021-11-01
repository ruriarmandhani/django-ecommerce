function addQuantity(e) {
  const elementId = `qty-${e.dataset.id}`;
  const quantity = document.getElementById(elementId).dataset.quantity;
  const stock = document.getElementById(elementId).dataset.stock;
  if (parseInt(quantity) < parseInt(stock)) {
    defaultChangeQtyURL = defaultChangeQtyURL
      .replace(/0/, e.dataset.id)
      .replace(/flag/, e.dataset.flag);
    location.href = defaultChangeQtyURL;
  } else {
    alert("Cannot be more than items in stock");
  }
}

function removeQuantity(e) {
  const elementId = `qty-${e.dataset.id}`;
  const quantity = document.getElementById(elementId).dataset.quantity;
  if (parseInt(quantity) - 1 < 1) {
    let isExecuted = confirm("Are you sure to remove this item?");
    if (isExecuted) {
      defaultChangeQtyURL = defaultChangeQtyURL
        .replace(/0/, e.dataset.id)
        .replace(/flag/, e.dataset.flag);
      location.href = defaultChangeQtyURL;
    }
  } else {
    defaultChangeQtyURL = defaultChangeQtyURL
      .replace(/0/, e.dataset.id)
      .replace(/flag/, e.dataset.flag);
    location.href = defaultChangeQtyURL;
  }
}
