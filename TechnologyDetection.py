import subprocess
import json
import re
import argparse


class TechnologyDetection:
    def __init__(self, target: str):
        """
        Initialize the TechnologyDetection object with the target URL, IP, or CIDR.
        :param target: The URL, IP address or CIDR to be analyzed.
        """
        self.target = target
        self.whatweb_output = ""

    def run_whatweb(self) -> str:
        """
        Run WhatWeb on the target and capture the output.
        :return: Raw output from the WhatWeb command.
        """
        try:
            # Running WhatWeb command to get technology information
            cmd = f"whatweb {self.target} --verbose"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.whatweb_output = result.stdout
                return self.whatweb_output
            else:
                raise Exception(f"Error running WhatWeb: {result.stderr}")
        
        except Exception as e:
            raise Exception(f"Failed to run WhatWeb: {str(e)}")

    def parse_output(self) -> dict:
        """
        Parse the raw output from WhatWeb and convert it into a structured JSON format.
        :return: Structured JSON data as a dictionary.
        """
        if not self.whatweb_output:
            raise ValueError("No output from WhatWeb to parse. Please run 'run_whatweb' first.")
        
        # Regex patterns for extracting the necessary data from the raw WhatWeb output
        status_pattern = re.compile(r"Status\s*:\s*(.*)")
        title_pattern = re.compile(r"Title\s*:\s*(.*)")
        ip_pattern = re.compile(r"IP\s*:\s*(.*)")
        country_pattern = re.compile(r"Country\s*:\s*(.*)")
        summary_pattern = re.compile(r"Summary\s*:\s*(.*)")
        plugins_pattern = re.compile(r"\[([^\]]+)\]\s*([\s\S]+?)(?=\[\w|\Z)")

        # Extract data using regular expressions
        status = re.search(status_pattern, self.whatweb_output)
        title = re.search(title_pattern, self.whatweb_output)
        ip = re.search(ip_pattern, self.whatweb_output)
        country = re.search(country_pattern, self.whatweb_output)
        summary = re.search(summary_pattern, self.whatweb_output)
        plugins = re.findall(plugins_pattern, self.whatweb_output)

        # Extract the technologies from the summary section
        technology_data = []
        if summary:
            # Split the technologies by commas and clean up the data
            technologies = summary.group(1).split(",")
            for tech in technologies:
                tech = tech.strip()
                # Split the technology from the version if available (e.g., Apache[2.4.56])
                tech_version_match = re.match(r"([a-zA-Z0-9\-]+)\[(.*?)\]", tech)
                if tech_version_match:
                    technology_data.append({
                        "technology": tech_version_match.group(1),
                        "version": tech_version_match.group(2)
                    })
                else:
                    # Only add the technology without version if version is unknown
                    technology_data.append({
                        "technology": tech
                    })

        # Format extracted data
        technologies = {
            "status": status.group(1) if status else "Unknown",
            "title": title.group(1) if title else "Unknown",
            "ip": ip.group(1) if ip else "Unknown",
            "country": country.group(1) if country else "Unknown",
            "technologies": technology_data,
            "plugins": [
                {
                    "name": plugin[0].strip(),
                    "description": plugin[1].strip()
                }
                for plugin in plugins
            ]
        }

        return technologies

    def get_technologies(self) -> dict:
        """
        Get a dictionary of technologies detected by WhatWeb.
        :return: A dictionary with technologies.
        """
        # Running WhatWeb and getting raw output
        self.run_whatweb()
        # Parsing the output and returning the result
        parsed_data = self.parse_output()
        
        return parsed_data


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run WhatWeb to detect technologies on a target.")
    parser.add_argument("target", help="The target to analyze (IP, domain, or CIDR).")
    
    args = parser.parse_args()
    
    # Create an instance of TechnologyDetection with the target provided by the user
    tech_detector = TechnologyDetection(args.target)

    try:
        # Get the technologies detected by WhatWeb
        techs = tech_detector.get_technologies()
        # Output the results in a structured JSON format
        print(json.dumps(techs, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
