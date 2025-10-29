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
    img.className = "w-full h-auto rounded";
    img.alt = item.image;

    card.appendChild(img);

    if (item.video) {
      const badge = document.createElement("div");
      badge.textContent = "LIVE";
      badge.className = "live-badge";
      card.appendChild(badge);

      const video = document.createElement("video");
      video.src = `/media/${item.video}`;
      video.className = "w-full h-auto rounded hidden";
      video.controls = false;
      video.muted = false;
      card.appendChild(video);

      const play = () => { video.classList.remove("hidden"); img.classList.add("hidden"); video.play(); };
      const stop = () => { video.pause(); video.classList.add("hidden"); img.classList.remove("hidden"); };

      card.addEventListener("pointerdown", play);
      card.addEventListener("pointerup", stop);
      card.addEventListener("mouseleave", stop);
      card.addEventListener("keydown", e => e.code === "Space" && play());
      card.addEventListener("keyup", e => e.code === "Space" && stop());
    }

    gallery.appendChild(card);
  }
}
loadGallery();
