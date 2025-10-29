// Prevent long-press save image menu on iOS
document.addEventListener(
	"contextmenu",
	(event) => {
		if (event.target.tagName === "IMG" || event.target.tagName === "VIDEO") {
			event.preventDefault();
		}
	},
	false
);

async function loadGallery() {
	const res = await fetch("/list");
	const items = await res.json();
	const gallery = document.getElementById("gallery");
	gallery.innerHTML = "";

	for (const item of items) {
		const card = document.createElement("div");
		card.className = "photo-card bg-white p-2";

		const img = document.createElement("img");
		img.src = `/media/${item.image}`;
		img.className = "photo-thumb";
		img.alt = item.image;
    img.draggable = false; // ✅ prevent iOS drag
		card.appendChild(img);

		if (item.video) {
			const video = document.createElement("video");
			video.src = `/media/${item.video}`;
			video.className = "photo-video";
			video.controls = false;
			video.muted = false;
			video.playsInline = true;
			card.appendChild(video);

			const badge = document.createElement("div");
			badge.textContent = "LIVE";
			badge.className = "live-badge";
			card.appendChild(badge);
			// Create overlay shimmer
			const overlay = document.createElement("div");
			overlay.className = "fade-overlay";
			card.appendChild(overlay);

			const play = () => {
				overlay.classList.add("active"); // shimmer in
				setTimeout(() => {
					video.style.opacity = "1";
					img.style.opacity = "0";
					video.play();
					badge.textContent = "LIVING";
          badge.classList.add("pulse");
					overlay.classList.remove("active"); // shimmer out
				}, 150);
			};

			const stop = () => {
				video.pause();
				overlay.classList.add("active");
				setTimeout(() => {
					video.style.opacity = "0";
					img.style.opacity = "1";
					badge.textContent = "LIVE";
          badge.classList.remove("pulse");
					overlay.classList.remove("active");
				}, 150);
			};

			// Interaction handlers
			card.addEventListener("pointerdown", play);
			card.addEventListener("pointerup", stop);
			card.addEventListener("mouseleave", stop);
			card.addEventListener("keydown", (e) => e.code === "Space" && play());
			card.addEventListener("keyup", (e) => e.code === "Space" && stop());
		}

		gallery.appendChild(card);
	}
}

loadGallery();
