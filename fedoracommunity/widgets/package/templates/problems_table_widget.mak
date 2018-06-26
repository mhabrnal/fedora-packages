<% import tg %>
<html>
<head></head>
<body>
<div class="list header-list">
    <table id="${w.id}" class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Crash function</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr class="">
                <td><a href="https://retrace.fedoraproject.org/faf/problems/${'${id}'}">${'${id}'}</a></td>
                <td>${'${status}'}</td>
                <td>${'${crash_function}'}</td>
                <td>${'${count}'}</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
