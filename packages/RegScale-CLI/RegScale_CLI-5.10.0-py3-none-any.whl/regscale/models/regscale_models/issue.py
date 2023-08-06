#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Issue """

# standard python imports
from typing import Any, List
from typing import Optional

from pydantic import BaseModel
from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger


class Issue(BaseModel):
    """Issue Model"""

    title: str = ""  # Required
    severityLevel: str = ""  # Required
    issueOwnerId: str = ""  # Required
    dueDate: str = ""  # Required
    id: Optional[int] = None
    uuid: Optional[str] = None
    dateCreated: Optional[str] = None
    description: Optional[str] = None
    issueOwner: Optional[str] = None
    costEstimate: Optional[int] = None
    levelOfEffort: Optional[int] = None
    identification: Optional[str] = None
    sourceReport: Optional[str] = None
    status: Optional[str] = None
    dateCompleted: Optional[str] = None
    activitiesObserved: Optional[str] = None
    failuresObserved: Optional[str] = None
    requirementsViolated: Optional[str] = None
    safetyImpact: Optional[str] = None
    securityImpact: Optional[str] = None
    qualityImpact: Optional[str] = None
    facility: Optional[str] = None
    facilityId: Optional[int] = None
    org: Optional[str] = None
    orgId: Optional[int] = None
    controlId: Optional[int] = None
    assessmentId: Optional[int] = None
    requirementId: Optional[int] = None
    securityPlanId: Optional[int] = None
    projectId: Optional[int] = None
    supplyChainId: Optional[int] = None
    policyId: Optional[int] = None
    componentId: Optional[int] = None
    incidentId: Optional[int] = None
    jiraId: Optional[str] = None
    serviceNowId: Optional[str] = None
    wizId: Optional[str] = None
    defenderId: Optional[str] = None
    defenderAlertId: Optional[str] = None
    defenderCloudId: Optional[str] = None
    prismaId: Optional[str] = None
    tenableId: Optional[str] = None
    qualysId: Optional[str] = None
    pluginId: Optional[str] = None
    cve: Optional[str] = None
    assetIdentifier: Optional[str] = None
    falsePositive: Optional[str] = None
    operationalRequirement: Optional[str] = None
    autoApproved: Optional[str] = None
    kevList: Optional[str] = None
    dateFirstDetected: Optional[str] = None
    changes: Optional[str] = None
    vendorDependency: Optional[str] = None
    vendorName: Optional[str] = None
    vendorLastUpdate: Optional[str] = None
    vendorActions: Optional[str] = None
    deviationRationale: Optional[str] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None
    createdBy: Optional[str] = None
    createdById: Optional[str] = None
    lastUpdatedBy: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    securityChecks: Optional[str] = None
    recommendedActions: Optional[str] = None
    isPublic: bool = True
    dependabotId: Optional[str] = None

    def __hash__(self):
        """
        Enable object to be hashable
        :return: Hashed TenableAsset
        """
        return hash(
            (
                self.title,
                self.parentId,
                self.parentModule,
                self.description,
            )
        )

    def __eq__(self, other) -> bool:
        """
        Return True if the two objects are equal
        :param other:
        :return: Updated Issue
        :rtype: bool
        """
        return (
            self.title == other.title
            and self.parentId == other.parentId
            and self.parentModule == other.parentModule
            and self.description == other.description
        )

    @staticmethod
    def assign_severity(value: Any = None) -> str:
        """
        Function to assign severity for an issue in RegScale using the provided value
        :param Any value: The value to analyze to determine the issue's severity, defaults to None
        :return: String of severity level for RegScale issue
        :rtype: str
        """
        severity_levels = {
            "low": "III - Low - Other Weakness",
            "moderate": "II - Moderate - Reportable Condition",
            "high": "I - High - Significant Deficiency",
        }
        severity = "IV - Not Assigned"
        # see if the value is an int or float
        if isinstance(value, (int, float)):
            # check severity score and assign it to the appropriate RegScale severity
            if value >= 7:
                severity = severity_levels["high"]
            elif 4 <= value < 7:
                severity = severity_levels["moderate"]
            else:
                severity = severity_levels["low"]
        elif isinstance(value, str):
            if value.lower() == "low":
                severity = severity_levels["low"]
            elif value.lower() in ["medium", "moderate"]:
                severity = severity_levels["moderate"]
            elif value.lower() in ["high", "critical"]:
                severity = severity_levels["high"]
            elif value in list(severity_levels.values()):
                severity = value
        return severity

    @staticmethod
    def update_issue(app: Application, issue: "Issue") -> "Issue":
        """Update an issue in RegScale"""
        api = Api(app)
        issue_id = issue.id

        response = api.put(
            app.config["domain"] + f"/api/issues/{issue_id}", json=issue.dict()
        )
        if response.status_code == 200:
            try:
                issue = Issue(**response.json())
            except JSONDecodeError:
                issue = None
        return issue

    @staticmethod
    def insert_issue(app: Application, issue: "Issue") -> "Issue":
        """Update an issue in RegScale"""
        api = Api(app)
        logger = create_logger()
        response = api.post(app.config["domain"] + "/api/issues", json=issue.dict())
        if response.status_code == 200:
            try:
                issue = Issue(**response.json())
            except JSONDecodeError as jex:
                logger.error("Unable to read issue:\n%s", jex)
                issue = None
        else:
            logger.warning("Unable to insert issue: %s", issue.title)
        return issue

    @staticmethod
    def fetch_issues_by_parent(
        app: Application,
        regscale_id: int,
        regscale_module: str,
    ) -> List["Issue"]:
        """
        Find all issues by parent id and parent module
        :param app: Application Instance
        :param parent_id: Parent ID
        :param parent_module: Parent Module
        :return: List of issues
        :rtype: List[issues]
        """
        app = Application()
        api = Api(app)
        body = """
                query {
                    issues(take: 50, skip: 0, where: { parentModule: {eq: "parent_module"} parentId: {
                      eq: parent_id
                    }}) {
                    items {
                        id
                        title
                        dateCreated
                        description
                        severityLevel
                        issueOwnerId
                        costEstimate
                        levelOfEffort
                        dueDate
                        identification
                        securityChecks
                        recommendedActions
                        sourceReport
                        status
                        dateCompleted
                        facilityId
                        orgId
                        controlId
                        assessmentId
                        requirementId
                        securityPlanId
                        projectId
                        supplyChainId
                        policyId
                        componentId
                        incidentId
                        jiraId
                        serviceNowId
                        wizId
                        prismaId
                        tenableId
                        qualysId
                        defenderId
                        defenderCloudId
                        pluginId
                        assetIdentifier
                        falsePositive
                        operationalRequirement
                        autoApproved
                        dateFirstDetected
                        changes
                        vendorDependency
                        vendorName
                        vendorLastUpdate
                        vendorActions
                        deviationRationale
                        parentId
                        parentModule
                        createdById
                        lastUpdatedById
                        dateLastUpdated
                        isPublic
                        dependabotId
                    },
                    pageInfo {
                        hasNextPage
                    }
                    ,totalCount}
                }
                    """.replace(
            "parent_module", regscale_module
        ).replace(
            "parent_id", str(regscale_id)
        )
        existing_regscale_issues = api.graph(query=body)["issues"]["items"]
        return [Issue(**issue) for issue in existing_regscale_issues]

    @staticmethod
    def fetch_issues_by_ssp(
        app: Application,
        ssp_id: int,
    ) -> List["Issue"]:
        """
        Find all issues by parent id and parent module
        :param app: Application Instance
        :param ssp_id: RegScale SSP Id
        :return: List of Issue
        :rtype: List[Issue]
        """
        api = Api(app)
        body = """
                query {
                    issues(take: 50, skip: 0, where: { securityPlanId: {eq: INVALID_SSP}}) {
                    items {
                        id
                        title
                        dateCreated
                        description
                        severityLevel
                        issueOwnerId
                        costEstimate
                        levelOfEffort
                        dueDate
                        identification
                        securityChecks
                        recommendedActions
                        sourceReport
                        status
                        dateCompleted
                        facilityId
                        orgId
                        controlId
                        assessmentId
                        requirementId
                        securityPlanId
                        projectId
                        supplyChainId
                        policyId
                        componentId
                        incidentId
                        jiraId
                        serviceNowId
                        wizId
                        prismaId
                        tenableId
                        qualysId
                        defenderId
                        defenderCloudId
                        pluginId
                        assetIdentifier
                        falsePositive
                        operationalRequirement
                        autoApproved
                        dateFirstDetected
                        changes
                        vendorDependency
                        vendorName
                        vendorLastUpdate
                        vendorActions
                        deviationRationale
                        parentId
                        parentModule
                        createdById
                        lastUpdatedById
                        dateLastUpdated
                        isPublic
                        dependabotId
                    },
                    pageInfo {
                        hasNextPage
                    }
                    ,totalCount}}
                    """.replace(
            "INVALID_SSP", str(ssp_id)
        )
        try:
            existing_issues = api.graph(query=body)["issues"]["items"]
        except JSONDecodeError:
            existing_issues = []
        return [Issue(**issue) for issue in existing_issues]
