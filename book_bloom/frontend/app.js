async function fetchBooks(query = "") {
  const url = query ? `/api/books/search?q=${encodeURIComponent(query)}` : "/api/books";
  const res = await fetch(url);
  const books = await res.json();
  const container = document.getElementById("books");
  container.innerHTML = "";
  for (const b of books) {
    const div = document.createElement("div");
    div.className = "book";
    div.innerHTML = `<h3>${b.title}</h3>
      <p>Author: ${b.author}</p>
      <p>ISBN: ${b.isbn ?? ""}</p>
      <p>Year: ${b.year_of_release ?? ""}</p>
      <p>Price: $${b.price ?? ""}</p>
      <p>Category: ${b.category ?? ""}</p>
      <p>State: ${b.state ?? ""}</p>`;
    container.appendChild(div);
  }
}

document.getElementById("search").addEventListener("input", (e) => {
  fetchBooks(e.target.value);
});

fetchBooks();
