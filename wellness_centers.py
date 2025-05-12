"""
Wellness center recommendations for mental health support.
This module provides information about wellness centers and mental health resources.
"""

def get_wellness_centers(location=None, count=3):
    """
    Get wellness center recommendations, optionally filtered by location.
    
    Args:
        location (str, optional): The location to filter centers by. Defaults to None.
        count (int, optional): Number of centers to return. Defaults to 3.
        
    Returns:
        list: A list of dictionaries containing wellness center information
    """
    # List of wellness centers with details
    centers = [
        {
            "name": "Mayo Clinic",
            "description": "Comprehensive medical and mental health services",
            "website": "https://www.mayoclinic.org/mental-health",
            "phone": "1-800-MAYO-CLINIC",
            "location": "Multiple locations across the US",
            "services": ["Psychiatry", "Psychology", "Therapy", "Counseling", "Addiction treatment"],
            "google_search": "https://www.google.com/search?q=mayo+clinic+mental+health+services"
        },
        {
            "name": "Cleveland Clinic Center for Behavioral Health",
            "description": "Comprehensive psychiatric and psychological services",
            "website": "https://my.clevelandclinic.org/departments/neurological/depts/behavioral-health",
            "phone": "866.588.2264",
            "location": "Cleveland, Ohio and other locations",
            "services": ["Psychiatry", "Psychology", "Therapy", "Counseling", "Addiction treatment"],
            "google_search": "https://www.google.com/search?q=cleveland+clinic+center+for+behavioral+health"
        },
        {
            "name": "McLean Hospital",
            "description": "Harvard Medical School Affiliate specializing in psychiatric care",
            "website": "https://www.mcleanhospital.org/",
            "phone": "617.855.2000",
            "location": "Belmont, Massachusetts",
            "services": ["Psychiatry", "Psychology", "Therapy", "Research", "Education"],
            "google_search": "https://www.google.com/search?q=mclean+hospital+mental+health"
        },
        {
            "name": "Hazelden Betty Ford Foundation",
            "description": "Addiction treatment and mental health services",
            "website": "https://www.hazeldenbettyford.org/",
            "phone": "1-866-831-5700",
            "location": "Multiple locations across the US",
            "services": ["Addiction treatment", "Mental health services", "Recovery support"],
            "google_search": "https://www.google.com/search?q=hazelden+betty+ford+foundation"
        },
        {
            "name": "Menninger Clinic",
            "description": "Psychiatric hospital specializing in treatment, research and education",
            "website": "https://www.menningerclinic.org/",
            "phone": "713-275-5000",
            "location": "Houston, Texas",
            "services": ["Psychiatry", "Psychology", "Therapy", "Research"],
            "google_search": "https://www.google.com/search?q=menninger+clinic"
        },
        {
            "name": "Sheppard Pratt",
            "description": "Psychiatric hospital and mental health system",
            "website": "https://www.sheppardpratt.org/",
            "phone": "410-938-3000",
            "location": "Baltimore, Maryland",
            "services": ["Psychiatry", "Psychology", "Therapy", "Counseling"],
            "google_search": "https://www.google.com/search?q=sheppard+pratt+mental+health"
        },
        {
            "name": "Timberline Knolls",
            "description": "Residential treatment center for women and girls",
            "website": "https://www.timberlineknolls.com/",
            "phone": "1-855-254-8326",
            "location": "Lemont, Illinois",
            "services": ["Eating disorders", "Addiction treatment", "Mood disorders", "Trauma recovery"],
            "google_search": "https://www.google.com/search?q=timberline+knolls+treatment+center"
        },
        {
            "name": "Rogers Behavioral Health",
            "description": "Specialized mental health and addiction services",
            "website": "https://rogersbh.org/",
            "phone": "800-767-4411",
            "location": "Multiple locations across the US",
            "services": ["OCD treatment", "Depression treatment", "Anxiety treatment", "Addiction treatment"],
            "google_search": "https://www.google.com/search?q=rogers+behavioral+health"
        },
        {
            "name": "Lindner Center of HOPE",
            "description": "Mental health center offering comprehensive treatment options",
            "website": "https://lindnercenterofhope.org/",
            "phone": "513-536-HOPE (4673)",
            "location": "Mason, Ohio",
            "services": ["Psychiatry", "Psychology", "Research", "Addiction treatment"],
            "google_search": "https://www.google.com/search?q=lindner+center+of+hope"
        },
        {
            "name": "The Meadows",
            "description": "Trauma and addiction treatment center",
            "website": "https://www.themeadows.com/",
            "phone": "800-244-4949",
            "location": "Wickenburg, Arizona",
            "services": ["Trauma treatment", "Addiction treatment", "Mental health services"],
            "google_search": "https://www.google.com/search?q=the+meadows+treatment+center"
        }
    ]
    
    # Filter by location if provided
    if location:
        location = location.lower()
        filtered_centers = [center for center in centers if location in center["location"].lower()]
        if filtered_centers:
            centers = filtered_centers
    
    # Return the requested number of centers (or all if count is greater than available)
    import random
    if count >= len(centers):
        return centers
    else:
        return random.sample(centers, count)

def get_online_resources(count=3):
    """
    Get online mental health resources.
    
    Args:
        count (int, optional): Number of resources to return. Defaults to 3.
        
    Returns:
        list: A list of dictionaries containing online resource information
    """
    resources = [
        {
            "name": "National Alliance on Mental Illness (NAMI)",
            "description": "Nation's largest grassroots mental health organization",
            "website": "https://www.nami.org/",
            "services": ["Education", "Advocacy", "Support groups", "Helpline"],
            "google_search": "https://www.google.com/search?q=national+alliance+on+mental+illness"
        },
        {
            "name": "Mental Health America",
            "description": "Community-based nonprofit dedicated to addressing mental health needs",
            "website": "https://www.mhanational.org/",
            "services": ["Screening tools", "Education", "Advocacy", "Support"],
            "google_search": "https://www.google.com/search?q=mental+health+america"
        },
        {
            "name": "Psychology Today Therapist Finder",
            "description": "Directory to find therapists, psychiatrists, and treatment centers",
            "website": "https://www.psychologytoday.com/us/therapists",
            "services": ["Therapist directory", "Treatment center directory"],
            "google_search": "https://www.google.com/search?q=psychology+today+therapist+finder"
        },
        {
            "name": "BetterHelp",
            "description": "Online counseling platform",
            "website": "https://www.betterhelp.com/",
            "services": ["Online therapy", "Counseling", "Support"],
            "google_search": "https://www.google.com/search?q=betterhelp+online+therapy"
        },
        {
            "name": "Talkspace",
            "description": "Online therapy platform",
            "website": "https://www.talkspace.com/",
            "services": ["Online therapy", "Psychiatry", "Couples therapy"],
            "google_search": "https://www.google.com/search?q=talkspace+online+therapy"
        }
    ]
    
    # Return the requested number of resources
    import random
    if count >= len(resources):
        return resources
    else:
        return random.sample(resources, count)

def format_wellness_center_recommendations(centers, include_online=True):
    """
    Format wellness center recommendations into a readable response.
    
    Args:
        centers (list): List of wellness center dictionaries
        include_online (bool, optional): Whether to include online resources. Defaults to True.
        
    Returns:
        str: Formatted response with wellness center recommendations
    """
    if not centers:
        return "I don't have any specific wellness center recommendations at the moment. You can search for 'mental health services near me' on Google: https://www.google.com/search?q=mental+health+services+near+me"
    
    response = "Here are some wellness centers and mental health resources that might be helpful:\n\n"
    
    for i, center in enumerate(centers, 1):
        response += f"{i}. {center['name']}\n"
        response += f"   {center['description']}\n"
        if 'location' in center:
            response += f"   Location: {center['location']}\n"
        if 'phone' in center:
            response += f"   Phone: {center['phone']}\n"
        response += f"   Website: {center['website']}\n"
        response += f"   Google Search: {center['google_search']}\n\n"
    
    if include_online:
        online_resources = get_online_resources(2)
        response += "Online Resources:\n\n"
        for i, resource in enumerate(online_resources, 1):
            response += f"{i}. {resource['name']}\n"
            response += f"   {resource['description']}\n"
            response += f"   Website: {resource['website']}\n"
            response += f"   Google Search: {resource['google_search']}\n\n"
    
    response += "Remember that this is not an exhaustive list, and I recommend searching for 'mental health services near me' on Google for more localized options: https://www.google.com/search?q=mental+health+services+near+me\n\n"
    response += "If you're experiencing a mental health emergency, please call the 988 Suicide & Crisis Lifeline at 988 or text HOME to 741741 to reach the Crisis Text Line."
    
    return response
