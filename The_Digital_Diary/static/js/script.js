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
