// static/js/participant.js
/**
 * 참여자 페이지 JavaScript
 * - 진도 체크
 * - 파일 업로드 처리
 */

// 진도 체크
document.querySelectorAll('.emotion-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const boxId = btn.dataset.boxId;
        const emotion = btn.dataset.emotion;
        
        try {
            const formData = new FormData();
            formData.append('emotion', emotion);
            formData.append('csrfmiddlewaretoken', CSRF_TOKEN);
            
            const response = await fetch(`/content/progress/${boxId}/add/`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // 같은 진도 박스의 다른 버튼 비활성화
                const parentBox = btn.closest('.progress-check');
                parentBox.querySelectorAll('.emotion-btn').forEach(b => {
                    b.classList.remove('active-happy', 'active-sad');
                });
                
                // 현재 버튼 활성화
                btn.classList.add(`active-${emotion}`);
                
                // 피드백 표시
                btn.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 200);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('진도 체크 중 오류가 발생했습니다.');
        }
    });
});

// Q&A 파일 선택 처리
const imageInput = document.getElementById('imageInput');
const questionInput = document.getElementById('questionInput');

if (imageInput && questionInput) {
    let selectedFile = null;
    
    imageInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            selectedFile = e.target.files[0];
            const fileName = selectedFile.name;
            
            const originalPlaceholder = questionInput.placeholder;
            questionInput.setAttribute('data-original-placeholder', originalPlaceholder);
            questionInput.placeholder = `📎 ${fileName} 첨부됨`;
        }
    });
    
    questionInput.addEventListener('focus', () => {
        const originalPlaceholder = questionInput.getAttribute('data-original-placeholder');
        if (originalPlaceholder && !questionInput.value) {
            questionInput.placeholder = originalPlaceholder;
        }
    });
    
    questionInput.addEventListener('blur', () => {
        if (imageInput.files && imageInput.files[0] && !questionInput.value) {
            questionInput.placeholder = `📎 ${imageInput.files[0].name} 첨부됨`;
        }
    });
}