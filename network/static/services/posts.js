export const putPost = (postId, content, csrftoken) => {
  console.log('putPost')
  return fetch(`/edit-post/${postId}`, {
    method: 'PUT',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({ content }),
    mode: 'same-origin',
  })
}
