class ActionClassifier:
    """
    Классифицирует действия по этапам пентеста
    """
    
    # Карта инструментов → этапы
    RECON_TOOLS = ['whois_checker', 'network_info', 'dns_enum', 'ping', 'nmap -sL']
    ENUMERATION_TOOLS = ['port_check', 'web_scanner', 'dir_buster', 'subdomain_scanner', 
                         'nmap -sV', 'nmap -sS', 'curl', 'wget', 'find', 'ls']
    ANALYSIS_TOOLS = ['ssl_checker', 'cve_lookup', 'grep', 'cat']
    EXPLOITATION_TOOLS = ['sql_tester', 'xss_scanner', 'hash_cracker', 'api_fuzzer']
    REPORTING_TOOLS = ['hl report', 'echo', 'cat', 'nano']
    
    @classmethod
    def classify(cls, command, tool='', target=''):
        """
        Определяет этап по команде и инструменту
        """
        # Если есть tool — используем его
        if tool:
            if tool in cls.RECON_TOOLS:
                return 'recon'
            if tool in cls.ENUMERATION_TOOLS:
                return 'enumeration'
            if tool in cls.ANALYSIS_TOOLS:
                return 'analysis'
            if tool in cls.EXPLOITATION_TOOLS:
                return 'exploitation'
            if tool in cls.REPORTING_TOOLS:
                return 'reporting'
        
        # Если tool нет — анализируем команду
        cmd_lower = command.lower()
        
        if any(t in cmd_lower for t in ['whois', 'ping', 'network', 'dns']):
            return 'recon'
        if any(t in cmd_lower for t in ['nmap', 'port', 'curl', 'wget', 'dir', 'subdomain']):
            return 'enumeration'
        if any(t in cmd_lower for t in ['ssl', 'cve', 'grep', 'cat', 'less']):
            return 'analysis'
        if any(t in cmd_lower for t in ['sql', 'xss', 'hash', 'fuzz']):
            return 'exploitation'
        if any(t in cmd_lower for t in ['report', 'echo', 'nano']):
            return 'reporting'
        
        return 'unknown'
    
    @classmethod
    def classify_actions(cls, actions):
        """
        Классифицирует список действий
        """
        classified = []
        for action in actions:
            command = action.get('command', '')
            tool = action.get('tool', '')
            target = action.get('target', '')
            stage = cls.classify(command, tool, target)
            classified.append({
                **action,
                'stage': stage
            })
        return classified
