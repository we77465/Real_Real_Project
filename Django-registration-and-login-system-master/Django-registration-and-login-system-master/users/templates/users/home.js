document.addEventListener("DOMContentLoaded", function() {
    const downloadButtons = document.querySelectorAll(".download-button");

    downloadButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const imageUrl = button.getAttribute("data-url");
            
            // 发送HTTP请求到Django视图
            fetch(`/download-image/?image_url=${encodeURIComponent(imageUrl)}`)
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    }
                    throw new Error('网络请求失败');
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'image.jpg';
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => {
                    console.error(error);
                });
        });
    });
});