from ai_assistant.core.models import Request
from ai_assistant.core.planners import BasePlanner
from .exceptions import MaxIterationsExceededError
from .execution_context import ExecutionContext
from .plan_executor import PlanExecutor


class AgentExecutionLoop:

    def __init__(
        self,
        planner: BasePlanner,
        executor: PlanExecutor,
        max_iterations: int = 10,
    ) -> None:
        
        if max_iterations < 1:
            raise ValueError(
                "max_iterations must be greater than 0."
            )
            
        self._planner = planner
        self._executor = executor
        self._max_iterations = max_iterations

    def execute(
        self,
        request: Request,
    ) -> ExecutionContext:

        context = ExecutionContext(
            request=request,
        )

        for _ in range(
            self._max_iterations,
        ):
            plan = self._planner.create_plan(
                request=request,
                previous_results=context.results,
            )

            context = self._executor.execute(
                plan=plan,
                request=request,
                context=context,
            )

            if context.is_completed():
                return context

        raise MaxIterationsExceededError(
            "Agent execution exceeded maximum iterations."
        )