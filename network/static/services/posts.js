export const putPost = (postId, content, csrftoken) => {
  return fetch(`/edit-post/${postId}`, {
    method: 'PUT',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({ content }),
    mode: 'same-origin',
  })
}

export const toggleLike = (postId, isLiked, csrftoken) => {
  return fetch(`post-likes/${postId}`, {
    method: 'PUT',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({ isLiked }),
    mode: 'same-origin',
  })
}