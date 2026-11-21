from agent.schemas import Posting

MOCK_POSTINGS = [
    # 0 - clear fit
    Posting(
        title="Python Automation Engineer",
        company="DataFlow",
        url="https://example.com/job/1",
        description="Build ETL pipelines and API integrations with Python, FastAPI and PostgreSQL. Docker deployments. Fully remote, EU timezones. 1-3 years experience or strong portfolio.",
        source="linkedin",
    ),
    # 1 - clear fit, AI-focused
    Posting(
        title="AI Automation Engineer",
        company="StartupXYZ",
        url="https://example.com/job/2",
        description="Build LLM-powered agents and workflow automation for customers. Python, REST APIs, OAuth integrations. Remote-first team, junior-friendly, portfolio matters more than degree.",
        source="company_site",
    ),
    # 2 - clear no: wrong stack, seniority, on-site
    Posting(
        title="Senior Java Developer",
        company="BigBank Inc",
        url="https://example.com/job/3",
        description="10+ years Java, Spring Boot, Oracle. On-site only in Frankfurt. Banking sector experience required.",
        source="indeed",
    ),
    # 3 - clear no: wrong field entirely
    Posting(
        title="Marketing Coordinator",
        company="RandomCo",
        url="https://example.com/job/4",
        description="Manage social media campaigns, write email newsletters, coordinate with design team. No technical skills required.",
        source="linkedin",
    ),
    # 4 - ambiguous: right stack, remote policy unclear
    Posting(
        title="Backend Developer",
        company="ShopIt",
        url="https://example.com/job/5",
        description="Python and Django backend for an e-commerce platform, some AI-powered recommendation features. Hybrid arrangement, office location not specified. 2+ years experience.",
        source="linkedin",
    ),
    # 5 - ambiguous: great title, but seniority likely out of reach
    Posting(
        title="Lead Automation Architect",
        company="ScaleOps",
        url="https://example.com/job/6",
        description="Own automation strategy across the org and manage a team of 5. Python, Kubernetes, Terraform, AWS. 7+ years required. Remote.",
        source="company_site",
    ),
    # 6 - trap: impressive title, wrong content
    Posting(
        title="AI Automation Specialist",
        company="CallCenterPro",
        url="https://example.com/job/7",
        description="Handle inbound customer calls and use our chatbot dashboard to escalate tickets. Shift work, on-site. No coding involved.",
        source="indeed",
    ),
    # 7 - ambiguous: relevant but vague, little information
    Posting(
        title="Junior Developer",
        company="TechNova",
        url="https://example.com/job/8",
        description="Join our growing engineering team. Work on exciting projects using modern technologies. Great benefits.",
        source="linkedin",
    ),
]

# What you'd expect the agent to decide. Use this to check its output later.
EXPECTED_DECISIONS = ["draft", "draft", "skip", "skip", "flag", "flag", "skip", "flag"]