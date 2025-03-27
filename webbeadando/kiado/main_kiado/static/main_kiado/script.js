document.querySelectorAll('.rating > label').forEach(star => {
    star.addEventListener('click', function () {
        const value = this.getAttribute('data-value');
        alert('Értékelés: ' + value + ' csillag');
    });
});
// document.addEventListener("DOMContentLoaded", function () {
//     const resultsContainer = document.getElementById('search-results');
//     const urlParams = new URLSearchParams(window.location.search);
//     const query = urlParams.get("q");

//     if (query) {
//         fetch(`/ajax/search/?q=${query}`, {
//             headers: {
//                 "X-Requested-With": "XMLHttpRequest"  // Jelöli, hogy ez egy AJAX kérés
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log("Kapott adatok:", data);  // Ellenőrzés a konzolban
//             displayResults(data);
//         })
//         .catch(error => {
//             console.error("Fetch hiba:", error);
//             resultsContainer.innerHTML = "<p>Hiba történt a keresés során.</p>";
//         });
//     }

//     function displayResults(data) {
//         let resultsHTML = '';

//         if (data.books.length > 0) {
//             resultsHTML += "<h4>Könyvek</h4><ul>";
//             data.books.forEach(book => {
//                 resultsHTML += `
//                     <li>
//                         <img src="/static/${book.cover_image || 'default-book.png'}" alt="${book.title}" style="width: 50px; height: 70px; margin-right: 10px;">
//                         <strong>${book.title}</strong> - ${book.author}
//                     </li>
//                 `;
//             });
//             resultsHTML += "</ul>";
//         }

//         if (data.employees.length > 0) {
//             resultsHTML += "<h4>Munkatársak</h4><ul>";
//             data.employees.forEach(employee => {
//                 resultsHTML += `
//                     <li>
//                         <strong>${employee.name}</strong> - ${employee.position}
//                     </li>
//                 `;
//             });
//             resultsHTML += "</ul>";
//         }

//         if (!data.books.length && !data.employees.length) {
//             resultsHTML = "<p>Nincs találat.</p>";
//         }

//         resultsContainer.innerHTML = resultsHTML;
//     }
// });
