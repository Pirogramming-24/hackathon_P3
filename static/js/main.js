// static/js/main.js
/**
 * 메인 페이지 공통 JavaScript
 * - 탭 전환
 * - 사이드바 제어
 */

// 현재 탭 정보 가져오기
const urlParams = new URLSearchParams(window.location.search);
const currentTab = urlParams.get('tab') || 'qa';

// 탭 전환
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        const isSessioner = document.body.dataset.isSessioner === 'true';
        const sessionId = document.body.dataset.sessionId;
        const urlPrefix = isSessioner ? '/sessioner' : '/participant';
        window.location.href = `${urlPrefix}/${sessionId}/?tab=${tabName}`;
    });
});

// 사이드바 토글
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

menuBtn.addEventListener('click', () => {
    sidebar.classList.add('show');
    sidebarOverlay.classList.add('show');
});

sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('show');
    sidebarOverlay.classList.remove('show');
});