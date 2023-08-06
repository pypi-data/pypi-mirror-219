from __future__ import annotations

from typing import Optional, Sequence, Union

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.client._constants import LIST_LIMIT_DEFAULT
from cognite.client.data_classes import TransformationNotification, TransformationNotificationList
from cognite.client.data_classes.transformations.notifications import TransformationNotificationFilter
from cognite.client.utils._identifier import IdentifierSequence


class TransformationNotificationsAPI(APIClient):
    _RESOURCE_PATH = "/transformations/notifications"

    def create(
        self, notification: Union[TransformationNotification, Sequence[TransformationNotification]]
    ) -> Union[TransformationNotification, TransformationNotificationList]:
        """`Subscribe for notifications on the transformation errors. <https://developer.cognite.com/api#tag/Transformation-Notifications/operation/createTransformationNotifications>`_

        Args:
            notification (Union[TransformationNotification, Sequence[TransformationNotification]]): Notification or list of notifications to create.

        Returns:
            Created notification(s)

        Examples:

            Create new notifications:

                >>> from cognite.client import CogniteClient
                >>> from cognite.client.data_classes import TransformationNotification
                >>> c = CogniteClient()
                >>> notifications = [TransformationNotification(transformation_id = 1, destination="my@email.com"), TransformationNotification(transformation_external_id="transformation2", destination="other@email.com"))]
                >>> res = c.transformations.notifications.create(notifications)
        """
        utils._auxiliary.assert_type(notification, "notification", [TransformationNotification, Sequence])
        return self._create_multiple(
            list_cls=TransformationNotificationList, resource_cls=TransformationNotification, items=notification
        )

    def list(
        self,
        transformation_id: Optional[int] = None,
        transformation_external_id: str = None,
        destination: str = None,
        limit: Optional[int] = LIST_LIMIT_DEFAULT,
    ) -> TransformationNotificationList:
        """`List notification subscriptions. <https://developer.cognite.com/api#tag/Transformation-Notifications/operation/getTransformationNotifications>`_

        Args:
            transformation_id (Optional[int]): Filter by transformation internal numeric ID.
            transformation_external_id (str): Filter by transformation externalId.
            destination (str): Filter by notification destination.
            limit (int): Limits the number of results to be returned. To retrieve all results use limit=-1, default limit is 25.

        Returns:
            TransformationNotificationList: List of transformation notifications

        Example:

            List all notifications::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> notifications_list = c.transformations.notifications.list()

            List all notifications by transformation id::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> notifications_list = c.transformations.notifications.list(transformation_id = 1)
        """
        filter = TransformationNotificationFilter(
            transformation_id=transformation_id,
            transformation_external_id=transformation_external_id,
            destination=destination,
        ).dump(camel_case=True)

        return self._list(
            list_cls=TransformationNotificationList,
            resource_cls=TransformationNotification,
            method="GET",
            limit=limit,
            filter=filter,
        )

    def delete(self, id: Union[int, Sequence[int]] = None) -> None:
        """`Deletes the specified notification subscriptions on the transformation. Does nothing when the subscriptions already don't exist <https://developer.cognite.com/api#tag/Transformation-Notifications/operation/deleteTransformationNotifications>`_

        Args:
            id (Union[int, Sequence[int]): Id or list of transformation notification ids

        Returns:
            None

        Examples:

            Delete schedules by id or external id::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> c.transformations.notifications.delete(id=[1,2,3])
        """
        self._delete_multiple(identifiers=IdentifierSequence.load(ids=id), wrap_ids=True)
