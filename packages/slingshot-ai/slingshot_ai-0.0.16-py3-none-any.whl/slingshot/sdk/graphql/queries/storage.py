from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ..base_graphql import BaseGraphQLQuery
from ..fragments import BlobArtifact, Volume


class BlobArtifactsResponse(BaseModel):
    blob_artifacts: list[BlobArtifact] = Field(..., alias="blobArtifacts")


class BlobArtifactsForProjectResponse(BaseModel):
    projects_by_pk: Optional[BlobArtifactsResponse] = Field(..., alias="projectsByPk")


class LatestBlobArtifactsForProjectQuery(BaseGraphQLQuery[BlobArtifactsForProjectResponse]):
    _query = """
        query LatestBlobArtifactsForProjectQuery($projectId: String!) {
            projectsByPk(projectId: $projectId) {
                blobArtifacts(orderBy: {createdAt: DESC}) {
                    ...BlobArtifact
                }
            }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=BlobArtifactsForProjectResponse)


class LatestBlobArtifactsForProjectByTagQuery(BaseGraphQLQuery[BlobArtifactsForProjectResponse]):
    _query = """
        query LatestBlobArtifactsForProjectQuery($projectId: String!, $tag: String = "") {
            projectsByPk(projectId: $projectId) {
                blobArtifacts(orderBy: {createdAt: DESC}, where: {tag: {_eq: $tag}}) {
                    ...BlobArtifact
                }
            }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, project_id: str, tag: str):
        super().__init__(
            variables={"projectId": project_id, "tag": tag}, response_model=BlobArtifactsForProjectResponse
        )


class BlobArtifactByIdResponse(BaseModel):
    blob_artifacts_by_pk: Optional[BlobArtifact] = Field(..., alias="blobArtifactsByPk")


class BlobArtifactByIdQuery(BaseGraphQLQuery[BlobArtifactByIdResponse]):
    _query = """
        query BlobArtifactById($blobArtifactId: String!) {
          blobArtifactsByPk(blobArtifactId: $blobArtifactId) {
            ...BlobArtifact
          }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, blob_artifact_id: str):
        super().__init__(variables={"blobArtifactId": blob_artifact_id}, response_model=BlobArtifactByIdResponse)


class BlobArtifactByNameResponse(BaseModel):
    blob_artifacts: list[BlobArtifact] = Field(..., alias="blobArtifacts")


class BlobArtifactByNameQuery(BaseGraphQLQuery[BlobArtifactByNameResponse]):
    _query = """
        query BlobArtifactByName($blobArtifactName: String!, $projectId: String!) {
          blobArtifacts(where: {_and: {name: {_eq: $blobArtifactName}, projectId: {_eq: $projectId}}}) {
            ...BlobArtifact
          }
        }
    """

    _depends_on = [BlobArtifact]

    def __init__(self, blob_artifact_name: str, project_id: str):
        super().__init__(
            variables={"blobArtifactName": blob_artifact_name, "projectId": project_id},
            response_model=BlobArtifactByNameResponse,
        )


class VolumesForProjectResponse(BaseModel):
    volumes: list[Volume] = Field(..., alias="volumes")


class VolumesForProjectQuery(BaseGraphQLQuery[VolumesForProjectResponse]):
    _query = """
        query VolumesForProject($projectId: String!) {
          volumes(where: {_and: {isArchived: {_eq: false}, projectId: {_eq: $projectId}}}) {
            ...Volume
          }
        } """

    _depends_on = [Volume]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=VolumesForProjectResponse)
