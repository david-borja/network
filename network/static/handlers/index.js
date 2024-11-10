import { putPost, toggleLike } from '../services/posts.js'
import { $, mimicDjangoDateString } from '../utils/index.js'

export const handleCancelEdit = (postId) => {
  const $editButton = $(`input[data-post='${postId}']`)
  $editButton.style.display = 'block'
  const $editFormContainer =
    $editButton.parentElement.querySelector('.edit-post')
  $editFormContainer.style.display = 'none'
  const $contentParagraph = $editButton.parentElement.querySelector('.content')
  $contentParagraph.style.display = 'block'
}

export const handleSubmitEdit = (postId, content) => {
  const $editButton = $(`input[data-post='${postId}']`)
  $editButton.style.display = 'block'
  const $editFormContainer =
    $editButton.parentElement.querySelector('.edit-post')
  $editFormContainer.style.display = 'none'
  const $contentParagraph = $editButton.parentElement.querySelector('.content')
  $contentParagraph.style.display = 'block'
  const csrftoken = $('[name=csrfmiddlewaretoken]').value

  putPost(postId, content, csrftoken)
    .then((response) => {
      if (response.ok) return response.json()
      else throw new Error('Failed to update post')
    })
    .then((data) => {
      $contentParagraph.innerText = content
      const $post = $editButton.parentElement
      let $editDate = $post.querySelector('.edit-date')
      if (!$editDate) {
        const $createdEditDate = document.createElement('span')
        $createdEditDate.classList.add('text-muted', 'mb-0', 'edit-date')
        $post.querySelector('.dates').appendChild($createdEditDate)
        $editDate = $createdEditDate
      }
      const lastEditDate = mimicDjangoDateString(data.lastEditDate)
      $editDate.innerText = `Edited on: ${lastEditDate}`
    })
    .catch((error) => {
      console.error(`Error: ${error.message}`)
    })
  return false
}

export const handleLikeClick = (postId, { isLiked }) => {
  const csrftoken = $('[name=csrfmiddlewaretoken]').value
  toggleLike(postId, !isLiked, csrftoken)
    .then((response) => {
      if (response.ok) {
        const $postCard = $(`div[data-post='${postId}']`)
        const likedSelector = '.like-button.liked'
        const notLikedSelector = '.like-button'
        const visibleButtonSelector = isLiked ? likedSelector : notLikedSelector
        const hiddenButtonSelector = isLiked ? notLikedSelector : likedSelector
        const $visibleLikeButton = $postCard.querySelector(
          visibleButtonSelector
        )
        const $hiddenLikeButton = $postCard.querySelector(
          hiddenButtonSelector
        )
        $visibleLikeButton.classList.add('d-none')
        $hiddenLikeButton.classList.remove('d-none')
        const $likesCount = $postCard.querySelector('.likes-count')
        const countAsString = $likesCount.innerText
        const count = parseInt(countAsString)
        $likesCount.innerText = isLiked ? Math.max(count - 1, 0) : count + 1
      } else throw new Error('Failed to like post')
    })
    .catch((error) => {
      console.error(`Error: ${error.message}`)
    })
}