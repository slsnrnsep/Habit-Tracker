function post() {
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }
    })
}

function get_posts(username) {
    if (username == undefined) {
        username = ""
    }
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)

                    let class_heart = post['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                    let class_star = post['star_by_me'] ? "fa-star" : "fa-star-o"
                    let class_like = post['like_by_me'] ? "fa-thumbs-up" : "fa-thumbs-o-up"

                    let html_temp = `<div class="swiper-slide">
                        <div class="card">
                            <div class="card-image">
                                <figure class="image is-4x3" style="width: 150px; margin: 5px auto;">
                                    <img class="is-rounded"
                                        src="{{ url_for('static', filename=user_info.profile_pic_real) }}"
                                        alt="Placeholder image">
                                </figure>
                            </div>

                            <div class="card-content">
                                <div class="media">
                                    <div class="media-left">
                                    </div>
                                    <div class="media-content">
                                        <p class="title is-4">{{ user_info.profile_name }}</p>
                                        <p class="subtitle is-6">
                                            <a href="user.html">@{{ user_info.username }}</a>
                                        </p>
                                    </div>
                                </div>

                                <div class="content">
                                    {{ user_info.profile_info }}
                                    사용자의 습관 요약
                                    <br>
                                    <br>
                                    <time datetime="2021-09-15">${작성시간 구현예정}</time>
                                </div>
                            </div>

                            <div class="button">
                                <button>습관체크하러가기</button>
                            </div>
                        </div>
                    </div>
                </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='${type}']`)
    let $i_like = $a_like.find("i")
    let class_s = {"heart": "fa-heart", "star": "fa-star", "like": "fa-thumbs-up"}
    let class_o = {"heart": "fa-heart-o", "star": "fa-star-o", "like": "fa-thumbs-o-up"}
    if ($i_like.hasClass(class_s[type])) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass(class_o[type]).removeClass(class_s[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass(class_s[type]).removeClass(class_o[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })

    }
}