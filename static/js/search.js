document.addEventListener('DOMContentLoaded', function() {
    // Desktop search elements
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchContainer = document.querySelector('.search-container');
    
    // Mobile search elements
    const mobileSearchForm = document.getElementById('mobile-search-form');
    const mobileSearchInput = document.getElementById('mobile-search-input');
    const mobileSearchResults = document.getElementById('mobile-search-results');
    const mobileSearchContainer = document.querySelector('.mobile-search-container');
    
    let searchTimeout;
    const minSearchLength = 3; // Minimum characters to trigger search

    // Setup search handlers for desktop
    setupSearchHandlers(searchForm, searchInput, searchResults, searchContainer);
    
    // Setup search handlers for mobile
    setupSearchHandlers(mobileSearchForm, mobileSearchInput, mobileSearchResults, mobileSearchContainer);

    // Sets up all event handlers for a search box (desktop or mobile)
    function setupSearchHandlers(form, input, results, container) {
        if (!form || !input || !results || !container) return;
        
        // Handle search input
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            const query = input.value.trim();
            
            // Clear results if query is too short
            if (query.length < minSearchLength) {
                results.innerHTML = '';
                results.classList.remove('show');
                return;
            }
            
            // Debounce the search request (wait 300ms after typing stops)
            searchTimeout = setTimeout(() => {
                fetchSearchResults(query, results);
            }, 300);
        });
        
        // Handle clicks outside the search area to close results
        document.addEventListener('click', function(event) {
            if (!container.contains(event.target)) {
                results.classList.remove('show');
            }
        });
        
        // Prevent form submission (we'll handle navigation via JS)
        form.addEventListener('submit', function(e) {
            const query = input.value.trim();
            if (query.length >= minSearchLength) {
                window.location.href = `/books/?q=${encodeURIComponent(query)}`;
                e.preventDefault();
            }
        });
        
        // Add focus event to the search input
        input.addEventListener('focus', function() {
            if (results.classList.contains('show')) {
                positionDropdown(results, container);
            }
        });
    }
    
    // Fetch search suggestions from the server
    function fetchSearchResults(query, resultsElement) {
        fetch(`/books/search/ajax/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                renderSearchResults(data.results, query, resultsElement);
                positionDropdown(resultsElement, resultsElement.closest('.search-results-container').parentElement);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
    }
    
    // Render search results in the dropdown
    function renderSearchResults(results, query, resultsElement) {
        resultsElement.innerHTML = '';
        
        if (results.length === 0) {
            resultsElement.innerHTML = '<div class="search-no-results">No results found</div>';
            resultsElement.classList.add('show');
            return;
        }
        
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item';
            
            resultItem.innerHTML = `
                <a href="${result.url}" class="search-result-link">
                    <div class="search-result-title">${highlightQuery(result.title, query)}</div>
                    <div class="search-result-meta">
                        <span class="search-result-author">${result.authors}</span>
                        <span class="search-result-price">£${result.price}</span>
                    </div>
                </a>
            `;
            
            resultsElement.appendChild(resultItem);
        });
        
        resultsElement.classList.add('show');
    }
    
    // Position the dropdown properly based on device
    function positionDropdown(resultsElement, container) {
        // Get screen size info
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
            // For mobile: position below the search form
            resultsElement.style.top = '100%';
            resultsElement.style.maxHeight = '60vh'; // Limit height on mobile
        } else {
            // For desktop/tablet: check if there's enough space below
            const containerRect = container.getBoundingClientRect();
            const spaceBelow = window.innerHeight - containerRect.bottom;
            
            if (spaceBelow < 300) {
                // Not enough space below, position above
                resultsElement.style.top = 'auto';
                resultsElement.style.bottom = '100%';
                resultsElement.style.maxHeight = (containerRect.top - 20) + 'px';
            } else {
                // Enough space below
                resultsElement.style.top = '100%';
                resultsElement.style.bottom = 'auto';
                resultsElement.style.maxHeight = '400px';
            }
        }
    }
    
    // Reposition dropdowns on window resize
    window.addEventListener('resize', function() {
        if (searchResults.classList.contains('show')) {
            positionDropdown(searchResults, searchContainer);
        }
        
        if (mobileSearchResults.classList.contains('show')) {
            positionDropdown(mobileSearchResults, mobileSearchContainer);
        }
    });
    
    // Highlight the search query in results
    function highlightQuery(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
});
