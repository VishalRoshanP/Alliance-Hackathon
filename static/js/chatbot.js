/* ============================================
   EduGuard - AI Chatbot Engine
   ============================================ */

const Chatbot = {
    isOpen: false,
    messages: [],

    knowledgeBase: {
        greetings: {
            patterns: ['hello', 'hi', 'hey', 'good morning', 'good evening', 'namaste', 'hii', 'helo'],
            responses: [
                "Hello! 👋 I'm EduGuard AI, your campus support assistant. How can I help you today?",
                "Hi there! 🌟 Welcome to EduGuard. I'm here to help with scholarships, academic advice, or any campus concerns. What do you need?",
                "Namaste! 🙏 I'm your EduGuard AI assistant. Ask me about schemes, academics, or report any issues you're facing."
            ]
        },
        scholarships: {
            patterns: ['scholarship', 'schemes', 'financial', 'money', 'fee', 'fund', 'aid', 'stipend', 'beti bachao', 'nsp', 'pragati'],
            responses: [
                "🎓 Here are some scholarships you might be eligible for:\n\n1. **Beti Bachao Beti Padhao** - ₹12,000/year for girls in classes 8-12\n2. **CBSE Merit Scholarship** - ₹25,000 for 80%+ scorers\n3. **NSP Post-Matric** - ₹15,000/year for minority students\n4. **Pragati (AICTE)** - ₹50,000/year for technical education\n\nWould you like details on any specific scholarship?",
                "💰 I can help you find the right scholarship! Based on your profile, I recommend checking:\n\n• **Beti Bachao Beti Padhao** scheme\n• **National Scholarship Portal** schemes\n• **State-level merit scholarships**\n\nTell me your class and marks, and I'll suggest the best options!"
            ]
        },
        academic: {
            patterns: ['study', 'exam', 'marks', 'grade', 'subject', 'homework', 'class', 'test', 'assignment', 'syllabus', 'tips', 'prepare'],
            responses: [
                "📚 Here are some study tips that can help:\n\n1. **Create a timetable** - Allocate fixed hours for each subject\n2. **Active recall** - Test yourself instead of passive reading\n3. **Pomodoro technique** - Study 25 mins, break 5 mins\n4. **Group study** - Discuss difficult topics with classmates\n5. **Mind maps** - Visualize concepts for better retention\n\nWould you like subject-specific advice?",
                "📖 For exam preparation, I suggest:\n\n• Start revision **2 weeks before** exams\n• Focus on **previous year papers**\n• Make **short notes** for quick revision\n• Get **8 hours of sleep** before exams\n• Practice **time management** during tests\n\nWhat subject are you struggling with?"
            ]
        },
        attendance: {
            patterns: ['attendance', 'absent', 'leave', 'present', 'bunk', 'miss class'],
            responses: [
                "📊 Attendance is crucial! Here's why:\n\n• Below **70% attendance** triggers an alert to your school authority\n• Regular attendance improves academic performance by **20-30%**\n• Many scholarships require **minimum 75% attendance**\n\nIf you're facing issues attending classes, please talk to your teacher or report it here. I can help connect you with support!",
                "⚠️ Maintaining good attendance is important for your academic journey. If you're missing classes due to:\n\n• **Health issues** - Get a medical certificate\n• **Family problems** - Talk to your counselor\n• **Transportation** - Report to administration\n• **Safety concerns** - Use the complaint system\n\nHow can I help you with your attendance?"
            ]
        },
        harassment: {
            patterns: ['bully', 'harass', 'threat', 'abuse', 'scared', 'unsafe', 'fear', 'ragging', 'touched', 'inappropriate'],
            responses: [
                "🛡️ I'm really sorry you're going through this. Your safety is our **top priority**.\n\n**Immediate steps:**\n1. You are **NOT alone** - this is not your fault\n2. **Report it** - I can help you file a confidential complaint\n3. **Tell someone you trust** - a teacher, parent, or counselor\n4. **Contact helpline**: Women Helpline **181** or Childline **1098**\n\nWould you like me to help you file a complaint? It will be treated with complete confidentiality. 💜",
                "💜 Your courage in speaking up matters. Here's what you can do:\n\n• **File a complaint** through this platform (it's confidential)\n• **Talk to the school counselor** - they're trained to help\n• **Emergency helplines**: Dial **112** for police, **181** for women helpline\n\nI can help you create a complaint right now. Your identity will be protected. Want to proceed?"
            ]
        },
        complaint: {
            patterns: ['complaint', 'report', 'issue', 'problem', 'grievance', 'concern', 'wrong'],
            responses: [
                "📝 I can help you report your concern. Please tell me:\n\n1. **What happened?** (Brief description)\n2. **Category**: Academic / Harassment / Hostel / General\n3. **When did it happen?**\n\nYour complaint will be submitted to the authorities and you can track its status from your dashboard. All complaints are treated confidentially.",
                "I'm here to help you report this issue. You can:\n\n• **Submit a complaint** through your dashboard\n• **Track existing complaints** to see their status\n• **Chat with me** for immediate guidance\n\nWhat would you like to report? I'll categorize and prioritize it for you."
            ]
        },
        hostel: {
            patterns: ['hostel', 'room', 'roommate', 'mess', 'food', 'warden', 'curfew', 'water', 'electricity'],
            responses: [
                "🏠 For hostel-related concerns:\n\n• **Maintenance issues** (water, electricity) - Report to warden\n• **Food quality** - Submit complaint in mess register\n• **Safety concerns** - File a complaint here for urgent attention\n• **Roommate issues** - Talk to hostel counselor\n\nI can help you file a formal complaint if the issue isn't resolved. What's the specific problem?"
            ]
        },
        dropout: {
            patterns: ['dropout', 'quit', 'leave school', 'stop study', 'not going', 'give up', 'can\'t study'],
            responses: [
                "💫 I understand things might feel tough right now, but **education is your superpower**.\n\n**Before you consider leaving:**\n• 📊 Girls with education earn **70% more** in their lifetime\n• 🎓 There are **scholarships** to help with financial issues\n• 🤝 **Counselors** can help with personal challenges\n• 📞 **Helplines** are available 24/7\n\nWhatever the reason, there's a solution. Tell me what's making it difficult, and let me help find a way forward. 🌈",
                "🌟 Please don't give up on your education! You have so much potential.\n\n**Common reasons & solutions:**\n• **Financial issues** → Scholarships & fee waivers available\n• **Family pressure** → Counseling services can help mediate\n• **Academic difficulties** → Extra tutoring and support available\n• **Safety concerns** → We can address them immediately\n\nLet's talk about what's troubling you. There's always a way! 💪"
            ]
        },
        mental_health: {
            patterns: ['sad', 'depressed', 'anxiety', 'stress', 'mental', 'lonely', 'cry', 'hopeless', 'help me', 'lost'],
            responses: [
                "💜 I hear you, and I want you to know that your feelings are valid.\n\n**You're not alone:**\n• 🧠 **iCall**: 9152987821 (Mon-Sat, 8am-10pm)\n• 📞 **Vandrevala Foundation**: 1860-2662-345 (24/7)\n• 🤝 **School counselor** - Request a session through your dashboard\n\n**Self-care tips:**\n• Talk to someone you trust\n• Practice deep breathing (4-7-8 technique)\n• Take small steps - one day at a time\n\nWant me to help you request a counseling session? 🌸"
            ]
        },
        thanks: {
            patterns: ['thanks', 'thank you', 'helpful', 'awesome', 'great', 'nice', 'appreciate'],
            responses: [
                "You're welcome! 😊 I'm always here to help. Don't hesitate to reach out anytime!",
                "Glad I could help! 🌟 Remember, your education journey matters. I'm here whenever you need me! 💜",
                "Happy to assist! 😄 Keep up the great work. You've got this! 💪"
            ]
        },
        goodbye: {
            patterns: ['bye', 'goodbye', 'see you', 'later', 'quit', 'exit'],
            responses: [
                "Goodbye! 👋 Stay safe and keep learning. I'm always here if you need me! 💜",
                "Take care! 🌈 Remember, you're stronger than you think. See you next time!"
            ]
        }
    },

    init() {
        this.renderChatbot();
        this.bindEvents();
        // Welcome message
        setTimeout(() => {
            this.addBotMessage("Hello! 👋 I'm **EduGuard AI**, your smart campus assistant. I can help you with:\n\n🎓 **Scholarships & Schemes**\n📚 **Academic Guidance**\n📝 **Report Issues**\n💜 **Emotional Support**\n\nHow can I help you today?");
        }, 500);
    },

    renderChatbot() {
        // Bubble
        const bubble = document.createElement('div');
        bubble.className = 'chatbot-bubble';
        bubble.id = 'chatbot-bubble';
        bubble.innerHTML = `🤖<span class="notification-dot"></span>`;
        document.body.appendChild(bubble);

        // Panel
        const panel = document.createElement('div');
        panel.className = 'chatbot-panel';
        panel.id = 'chatbot-panel';
        panel.innerHTML = `
      <div class="chatbot-header">
        <div class="bot-avatar">🤖</div>
        <div class="bot-info">
          <h4>EduGuard AI</h4>
          <span class="bot-status">Online</span>
        </div>
        <button class="chatbot-close" id="chatbot-close">✕</button>
      </div>
      <div class="chatbot-messages" id="chatbot-messages"></div>
      <div class="quick-replies" id="quick-replies">
        <button class="quick-reply-btn" data-msg="Find Scholarships">🎓 Find Scholarships</button>
        <button class="quick-reply-btn" data-msg="Academic Help">📚 Academic Help</button>
        <button class="quick-reply-btn" data-msg="Report an Issue">📝 Report Issue</button>
        <button class="quick-reply-btn" data-msg="I need support">💜 Support</button>
      </div>
      <div class="chatbot-input-area">
        <input type="text" id="chatbot-input" placeholder="Type your message..." autocomplete="off">
        <button class="chatbot-send-btn" id="chatbot-send">➤</button>
      </div>
    `;
        document.body.appendChild(panel);
    },

    bindEvents() {
        document.getElementById('chatbot-bubble').addEventListener('click', () => this.toggle());
        document.getElementById('chatbot-close').addEventListener('click', () => this.toggle());
        document.getElementById('chatbot-send').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Quick replies
        document.querySelectorAll('.quick-reply-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('chatbot-input').value = btn.dataset.msg;
                this.sendMessage();
            });
        });
    },

    toggle() {
        this.isOpen = !this.isOpen;
        const panel = document.getElementById('chatbot-panel');
        const bubble = document.getElementById('chatbot-bubble');
        panel.classList.toggle('open', this.isOpen);
        bubble.querySelector('.notification-dot').style.display = this.isOpen ? 'none' : 'block';
        if (this.isOpen) {
            document.getElementById('chatbot-input').focus();
        }
    },

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const text = input.value.trim();
        if (!text) return;

        this.addUserMessage(text);
        input.value = '';

        // Show typing indicator
        this.showTyping();

        // Generate response after delay
        setTimeout(() => {
            this.hideTyping();
            const response = this.generateResponse(text);
            this.addBotMessage(response);
        }, 800 + Math.random() * 800);
    },

    addUserMessage(text) {
        const container = document.getElementById('chatbot-messages');
        const msg = document.createElement('div');
        msg.className = 'chat-message user';
        msg.innerHTML = `
      <div class="message-bubble">${this.escapeHtml(text)}</div>
      <div class="message-time">${formatTime(new Date())}</div>
    `;
        container.appendChild(msg);
        container.scrollTop = container.scrollHeight;
    },

    addBotMessage(text) {
        const container = document.getElementById('chatbot-messages');
        const msg = document.createElement('div');
        msg.className = 'chat-message bot';
        msg.innerHTML = `
      <div class="message-bubble">${this.formatMarkdown(text)}</div>
      <div class="message-time">${formatTime(new Date())}</div>
    `;
        container.appendChild(msg);
        container.scrollTop = container.scrollHeight;
    },

    showTyping() {
        const container = document.getElementById('chatbot-messages');
        const typing = document.createElement('div');
        typing.className = 'chat-message bot';
        typing.id = 'typing-indicator';
        typing.innerHTML = `
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    `;
        container.appendChild(typing);
        container.scrollTop = container.scrollHeight;
    },

    hideTyping() {
        const typing = document.getElementById('typing-indicator');
        if (typing) typing.remove();
    },

    generateResponse(input) {
        const lower = input.toLowerCase();
        let bestMatch = null;
        let bestScore = 0;

        for (const [category, data] of Object.entries(this.knowledgeBase)) {
            for (const pattern of data.patterns) {
                if (lower.includes(pattern)) {
                    const score = pattern.length;
                    if (score > bestScore) {
                        bestScore = score;
                        bestMatch = data.responses;
                    }
                }
            }
        }

        if (bestMatch) {
            return bestMatch[Math.floor(Math.random() * bestMatch.length)];
        }

        // Default responses
        const defaults = [
            "I understand your concern. Could you provide more details so I can assist you better? You can ask me about:\n\n🎓 Scholarships\n📚 Academic help\n📝 Report complaints\n💜 Emotional support",
            "Thank you for reaching out! I'm here to help. Try asking about scholarships, study tips, or reporting any campus issues.",
            "I want to make sure I help you properly. Could you rephrase your question? I'm best at helping with education schemes, academic guidance, and campus safety."
        ];
        return defaults[Math.floor(Math.random() * defaults.length)];
    },

    formatMarkdown(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
