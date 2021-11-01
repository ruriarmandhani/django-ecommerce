const colorElements = document.getElementsByName("filter-color");
const urlSearchParams = new URLSearchParams(location.search);
const params = Object.fromEntries(urlSearchParams.entries());

function applyPriceFilter() {
  if (
    parseInt(document.getElementById("min-price").value) >
    parseInt(document.getElementById("max-price").value)
  ) {
    alert("Maximum price cannot be less than minimum price.");
  } else if (Object.keys(params).length >= 1) {
    const min = document.getElementById("min-price").value;
    const max = document.getElementById("max-price").value;
    location.href += `&min-price=${min}&max-price${max}`;
  } else {
    location.href = `?min-price=${min}&max-price${max}`;
  }
}

document.getElementById("min-price").addEventListener("keydown", function (e) {
  if (
    ((parseInt(e.key) >= 0) & (parseInt(e.key) <= 9)) |
    (e.key == "Backspace") |
    (e.key == "Tab")
  ) {
    return true;
  }
  e.preventDefault();
});

document.getElementById("max-price").addEventListener("keydown", function (e) {
  if (
    ((parseInt(e.key) >= 0) & (parseInt(e.key) <= 9)) |
    (e.key == "Backspace") |
    (e.key == "Tab")
  ) {
    return true;
  }
  e.preventDefault();
});

if (
  Object.keys(params).includes("min-price") &
  Object.keys(params).includes("max-price")
) {
  document.getElementById("min-price").value = params["min-price"];
  document.getElementById("max-price").value = params["max-price"];
}

if (Object.keys(params).includes("color") == true) {
  document.getElementById("collapseTwo").classList.add("show");
  const colors = params["color"].split(",");
  colorElements.forEach((e) => {
    if (colors.includes(e.value)) {
      e.checked = true;
    }
  });
}

if (Object.keys(params).includes("sort-by") == true) {
  document.getElementById("sort").value = params["sort-by"];
}

function colorFilter(e) {
  const color = e.value;

  if ((Object.keys(params).includes("color") == false) & (e.checked == true)) {
    if (Object.keys(params).length <= 0) {
      location.href = `?color=${color}`;
    } else {
      location.href += `&color=${color}`;
    }
  } else if (
    (Object.keys(params).includes("color") == true) &
    (e.checked == true)
  ) {
    let colors = params["color"].split(",");
    if (colors.includes(color) == false) {
      colors.push(color);
    }
    const colorText = colors.join();
    if (Object.keys(params)[0] == "color") {
      location.href = location.href.replace(
        `?color=${params["color"]}`,
        `?color=${colorText}`
      );
    } else {
      location.href = location.href.replace(
        `&color=${params["color"]}`,
        `&color=${colorText}`
      );
    }
  } else if (
    (Object.keys(params).includes("color") == true) &
    (e.checked == false)
  ) {
    let colors = params["color"].split(",");
    if (colors.includes(color) == true) {
      const idxColor = colors.indexOf(color);
      colors.splice(idxColor, 1);
    }
    if (
      (colors.length < 1) &
      (Object.keys(params).length <= 1) &
      (Object.keys(params)[0] == "color")
    ) {
      console.log("Halo");
      location.href = location.href.replace(`?color=${params["color"]}`, "");
    } else if (
      (colors.length < 1) &
      (Object.keys(params).length > 1) &
      (Object.keys(params)[0] == "color")
    ) {
      console.log(params);
      location.href = location.href.replace(`?color=${params["color"]}&`, "?");
    } else if (
      (colors.length < 1) &
      (Object.keys(params).length > 0) &
      (Object.keys(params)[0] != "color")
    ) {
      location.href = location.href.replace(`&color=${params["color"]}`, "");
    } else if ((colors.length >= 1) & (Object.keys(params)[0] == "color")) {
      location.href = location.href.replace(
        `?color=${params["color"]}`,
        `?color=${colors}`
      );
    } else if ((colors.length >= 1) & (Object.keys(params)[0] != "color")) {
      location.href = location.href.replace(
        `&color=${params["color"]}`,
        `&color=${colors}`
      );
    } else {
      location.href = `?color=${colors}`;
    }
  }
}

function sortItem(e) {
  const sortBy = e.value;
  if (
    (Object.keys(params).includes("sort-by") == false) &
    (Object.keys(params).length >= 1)
  ) {
    location.href += `&sort-by=${sortBy}`;
  } else if (
    (Object.keys(params).includes("sort-by") == true) &
    (Object.keys(params).length >= 1)
  ) {
    location.href = location.href.replace(params["sort-by"], sortBy);
  } else {
    location.href = `?sort-by=${sortBy}`;
  }
}
