$(document).ready(function() {
function validateSearch() {
    const input = document.querySelector('input[name="q"]');
    if (input.value.trim() === "") {
        // Prevent form submission
        return false;
    }
    return true;
}
$(document).ready(function () {
	$(".icon-wrap").click(function () {
		$(this).toggleClass("open");
		const isOpen = $(this).hasClass("open");
		
		if (isOpen) {
			$(".form-control").focus();
			$(this).find("svg").css({ fill: "#737272", transform: "rotate(90deg)" });
			$(".label-wrap").animate({ opacity: 0 }, 100);
		} else {
			$(".form-control").blur();
			$(this).find("svg").css({ fill: "#000", transform: "rotate(0deg)" });
			$(".label-wrap").animate({ opacity: 1 }, 1200);
		}
	});

	$("input").focus(function () {
		$(".label-wrap").animate({ opacity: 0 }, 100);
	});
	$("input").blur(function () {
		if ($(this).val() === "") {
			$(".label-wrap").animate({ opacity: 1 }, 1200);
		}
	});
});


    $(document).ready(function () {
        $('.search-button').click(function () {
            // Example: Add animation or any specific logic here
        });
    });

	//like btn

	document.getElementById('like-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const likeBtn = document.getElementById('like-btn');
    const errorDiv = document.getElementById('like-error');
    const url = likeBtn.parentElement.action;  // Get form action URL

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',  // Include CSRF token
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            likeBtn.innerText = `Like (${data.total_likes})`;
            errorDiv.style.display = 'none';  // Hide error message if success
        } else {
            displayError(data.error || 'Unable to update like count.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayError('An error occurred while liking the post.');
    });
});

function displayError(message) {
    const errorDiv = document.getElementById('like-error');
    errorDiv.innerText = message;
    errorDiv.style.display = 'block';
}

	
	






});