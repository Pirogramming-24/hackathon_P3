// static/js/initial.js
/**
 * 초기 화면 JavaScript
 * - 드롭다운 메뉴 제어
 * - 세션 선택 및 페이지 이동
 */

let selectedSessionId = null;

const dropdownButton = document.getElementById('dropdownButton');
const dropdownMenu = document.getElementById('dropdownMenu');
const dropdownText = document.getElementById('dropdownText');
const dropdownArrow = document.querySelector('.dropdown-arrow');
const participantBtn = document.getElementById('participantBtn');
const sessionerBtn = document.getElementById('sessionerBtn');

// 드롭다운 토글
dropdownButton.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show');
    dropdownButton.classList.toggle('active');
    dropdownArrow.classList.toggle('rotate');
});

// 드롭다운 아이템 선택
document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', () => {
        selectedSessionId = item.dataset.id;
        const title = item.dataset.title;
        const date = item.dataset.date;
        
        dropdownText.textContent = `${title} (${date})`;
        dropdownText.classList.add('selected');
        dropdownMenu.classList.remove('show');
        dropdownButton.classList.remove('active');
        dropdownArrow.classList.remove('rotate');
    });
});

// 외부 클릭시 드롭다운 닫기
document.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown')) {
        dropdownMenu.classList.remove('show');
        dropdownButton.classList.remove('active');
        dropdownArrow.classList.remove('rotate');
    }
});

// 참여자 버튼
participantBtn.addEventListener('click', () => {
    if (!selectedSessionId) {
        alert('세션 날짜를 선택해주세요');
        return;
    }
    window.location.href = `/participant/${selectedSessionId}/`;
});

// 세션자 버튼
sessionerBtn.addEventListener('click', () => {
    if (!selectedSessionId) {
        alert('세션 날짜를 선택해주세요');
        return;
    }
    window.location.href = `/sessioner/${selectedSessionId}/`;
});