load('config.js');

function execute(key, page) {
    if (!page) page = '1';

    // Tạo URL mobile từ BASE_URL (Ví dụ: từ tranh18.com thành m.tranh18.com)
    // Nếu BASE_URL đã có https:// thì ta chèn 'm.' vào sau nó.
    let mobileHost = BASE_URL.replace("://", "://m.");
    
    // URL tìm kiếm sử dụng host mobile
    let url = `${mobileHost}/search?keyword=${encodeURIComponent(key)}&page=${page}`;
    
    let response = fetch(url);
    
    if (response.ok) {
        let doc = response.html();
        let data = [];
        
        // Duyệt qua danh sách kết quả (theo cấu trúc HTML mobile đã phân tích)
        doc.select("ul.book-list li").forEach(e => {
            let info = e.select(".book-list-info");
            let aTag = info.select("a").first();
            let imgTag = e.select("img.book-list-cover-img").first();

            // Link truyện: Chúng ta CHUYỂN NGƯỢC về BASE_URL gốc (tranh18.com)
            // để khớp với detail.js và home.js của ứng dụng
            let rawLink = aTag.attr("href");
            let link = rawLink;
            if (link && !link.startsWith("http")) {
                link = BASE_URL + (link.startsWith("/") ? "" : "/") + link;
            } else if (link) {
                // Nếu link trả về có m. thì xóa nó đi để đồng bộ với config.js
                link = link.replace("://m.", "://");
            }

            // Ảnh bìa: Lấy từ mobileHost vì ảnh thường nằm trên server đó
            let coverUrl = imgTag.attr("data-original") || imgTag.attr("src");
            if (coverUrl && !coverUrl.startsWith("http")) {
                coverUrl = mobileHost + (coverUrl.startsWith("/") ? "" : "/") + coverUrl;
            }

            data.push({
                name: aTag.select(".book-list-info-title").text(),
                link: link,          // Đã đưa về tranh18.com
                cover: coverUrl,
                description: info.select(".book-list-info-bottom-item").text(),
                host: BASE_URL      // Trả về host gốc tranh18.com
            });
        });

        // Phân trang
        let next = (data.length > 0) ? (parseInt(page) + 1).toString() : null;

        return Response.success(data, next);
    }
    
    return null;
}
