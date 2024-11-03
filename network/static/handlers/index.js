import { putPost } from '../services/posts.js'
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
