// static/js/sessioner.js
/**
 * 세션자 페이지 JavaScript
 * - 답변 폼 토글
 * - 답변 완료 상태 토글
 * - 파일 업로드 처리
 */

// 답변 폼 토글
function toggleReplyForm(questionId) {
    const form = document.getElementById(`reply-form-${questionId}`);
    if (form) {
        if (form.style.display === 'none') {
            form.style.display = 'block';
            const input = form.querySelector('input[name="reply"]');
            if (input) input.focus();
        } else {
            form.style.display = 'none';
        }
    }
}

// 답변 완료 상태 토글
async function toggleAnswered(questionId) {
    try {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', CSRF_TOKEN);
        
        const response = await fetch(`/question/${questionId}/toggle/`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            const btn = document.getElementById(`status-btn-${questionId}`);
            const icon = document.getElementById(`status-icon-${questionId}`);
            
            // 아이콘 변경
            if (data.answered) {
                btn.classList.add('answered');
                icon.innerHTML = '<polyline points="20 6 9 17 4 12"></polyline>';
            } else {
                btn.classList.remove('answered');
                icon.innerHTML = '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('상태 변경 중 오류가 발생했습니다.');
    }
}

// Contents 파일 선택 처리
const contentFile = document.getElementById('contentFile');
const contentInput = document.getElementById('contentInput');

if (contentFile && contentInput) {
    let selectedContentFile = null;
    
    contentFile.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            selectedContentFile = e.target.files[0];
            const fileName = selectedContentFile.name;
            
            const originalPlaceholder = contentInput.placeholder;
            contentInput.setAttribute('data-original-placeholder', originalPlaceholder);
            contentInput.placeholder = `📎 ${fileName} 첨부됨`;
        }
    });
    
    contentInput.addEventListener('focus', () => {
        const originalPlaceholder = contentInput.getAttribute('data-original-placeholder');
        if (originalPlaceholder && !contentInput.value) {
            contentInput.placeholder = originalPlaceholder;
        }
    });
    
    contentInput.addEventListener('blur', () => {
        if (selectedContentFile && !contentInput.value) {
            contentInput.placeholder = `📎 ${selectedContentFile.name} 첨부됨`;
        }
    });
}

// Notice 파일 선택 처리
const noticeFile = document.getElementById('noticeFile');
const noticeFileName = document.getElementById('noticeFileName');

if (noticeFile && noticeFileName) {
    noticeFile.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const fileName = e.target.files[0].name;
            noticeFileName.textContent = fileName;
        }
    });
}